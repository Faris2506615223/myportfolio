"""Assignment 6: API contracts, four roles, database integrity and real CSRF."""

import re
import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient, APITestCase

from main.models import Experience
from main.serializers import ExperienceSerializer


class ExperienceAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="owner6", password="test-password", email="private@example.com",
        )
        cls.regular = User.objects.create_user(username="regular6", password="test-password")
        cls.editor = User.objects.create_user(username="editor6", password="test-password")
        cls.staff = User.objects.create_user(
            username="staff6", password="test-password", is_staff=True,
        )
        group, _ = Group.objects.get_or_create(name="Editor")
        cls.editor.groups.add(group)
        cls.experience = Experience.objects.create(
            title="Asisten Dosen PBP", description="Membantu praktikum Django.",
            category="part-time", thumbnail="https://example.com/teaching.jpg",
        )

    def setUp(self):
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.pk])
        self.star_url = reverse("api:experience-star", args=[self.experience.pk])
        self.payload = {
            "title": "Mentor Pemrograman", "description": "Mengajar Python untuk pemula.",
            "category": "volunteer", "thumbnail": "https://example.com/mentor.jpg",
        }

    def database_snapshot(self):
        """A rejected request must preserve both content and star membership."""
        return (
            list(Experience.objects.order_by("id").values()),
            list(Experience.starred_by.through.objects.order_by("id").values()),
        )

    def test_every_role_can_read_list_detail_and_head(self):
        for user in (None, self.regular, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data[0]["id"], str(self.experience.pk))
                self.assertEqual(self.client.get(self.detail_url).status_code, 200)
                self.assertEqual(self.client.head(self.list_url).status_code, 200)
                self.assertEqual(self.client.head(self.detail_url).status_code, 200)

    def test_search_category_status_and_combined_filters(self):
        completed = Experience.objects.create(
            title="Mentor Python", description="Kelas komunitas.", category="volunteer",
            ended_at=timezone.now(),
        )
        cases = [
            ({"title": "  DOSEN  "}, [str(self.experience.pk)]),
            ({"title": "tidak-ada"}, []),
            ({"category": "volunteer"}, [str(completed.pk)]),
            ({"status": "ongoing"}, [str(self.experience.pk)]),
            ({"status": "completed"}, [str(completed.pk)]),
            ({"title": "mentor", "category": "volunteer", "status": "completed"}, [str(completed.pk)]),
            ({"title": "mentor", "status": "ongoing"}, []),
        ]
        for params, expected in cases:
            with self.subTest(params=params):
                response = self.client.get(self.list_url, params)
                self.assertEqual(response.status_code, 200)
                self.assertEqual([item["id"] for item in response.data], expected)

    def test_empty_list_is_an_array(self):
        Experience.objects.all().delete()
        self.assertEqual(self.client.get(self.list_url).data, [])

    def test_public_fields_and_star_metadata_do_not_expose_account_details(self):
        self.experience.starred_by.add(self.owner)
        response = self.client.get(self.detail_url)
        self.assertEqual(set(response.data), set(ExperienceSerializer.Meta.fields))
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], self.owner.username)
        self.assertEqual(response.data["category_display"], "Part-Time")
        self.assertTrue(response.data["is_ongoing"])
        for private_value in (self.owner.email, self.owner.password):
            self.assertNotContains(response, private_value)
        for private_key in ("email", "password", "starred_by", "user_id"):
            self.assertNotIn(private_key, response.data)
        self.client.force_authenticate(user=self.owner)
        self.assertTrue(self.client.get(self.detail_url).data["is_starred"])

    def test_guest_regular_and_staff_cannot_write_and_database_is_unchanged(self):
        for user in (None, self.regular, self.staff):
            self.client.force_authenticate(user=user)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"title": "Unauthorized"}),
                ("delete", self.detail_url, {}),
            ):
                with self.subTest(user=user, method=method):
                    before = self.database_snapshot()
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, 403)
                    self.assertEqual(self.database_snapshot(), before)

    def test_editor_cannot_create_or_delete_and_database_is_unchanged(self):
        self.client.force_authenticate(user=self.editor)
        for method, url in (("post", self.list_url), ("delete", self.detail_url)):
            with self.subTest(method=method):
                before = self.database_snapshot()
                response = getattr(self.client, method)(url, self.payload, format="json")
                self.assertEqual(response.status_code, 403)
                self.assertEqual(self.database_snapshot(), before)

    def test_editor_patch_changes_only_supplied_fields(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"title": "<b>Asisten PBP</b>"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten PBP")
        self.assertEqual(self.experience.description, "Membantu praktikum Django.")
        self.assertEqual(self.experience.category, "part-time")

    def test_editor_can_put_a_complete_representation(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        for field, value in self.payload.items():
            self.assertEqual(getattr(self.experience, field), value)

    def test_owner_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        created_id = response.data["id"]
        self.assertTrue(Experience.objects.filter(pk=created_id).exists())
        url = reverse("api:experience-detail", args=[created_id])
        self.assertEqual(self.client.patch(url, {"title": "Mentor UI"}, format="json").status_code, 200)
        self.assertEqual(self.client.put(url, self.payload, format="json").status_code, 200)
        deleted = self.client.delete(url)
        self.assertEqual(deleted.status_code, 204)
        self.assertEqual(deleted.content, b"")
        self.assertFalse(Experience.objects.filter(pk=created_id).exists())
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_put_requires_all_required_fields_and_rejection_is_atomic(self):
        self.client.force_authenticate(user=self.owner)
        before = self.database_snapshot()
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("description", response.data)
        self.assertIn("category", response.data)
        self.assertEqual(self.database_snapshot(), before)

    def test_put_resets_optional_thumbnail_when_omitted(self):
        self.client.force_authenticate(user=self.owner)
        payload = {key: value for key, value in self.payload.items() if key != "thumbnail"}
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.thumbnail, "")

    def test_create_strips_html_and_whitespace(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "title": " <b>Mentor</b> ",
            "description": '<img src="x" onerror="alert(1)"> Mengajar <em>Python</em>.',
        }, format="json")
        self.assertEqual(response.status_code, 201)
        saved = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(saved.title, "Mentor")
        self.assertEqual(saved.description, "Mengajar Python.")

    def test_invalid_input_returns_field_errors_without_creating_data(self):
        self.client.force_authenticate(user=self.owner)
        for field, value in (
            ("title", "<b></b>"), ("title", "x" * 256),
            ("description", "<img src=x onerror=alert(1)>"),
            ("description", "   "), ("category", "unknown"),
            ("thumbnail", "javascript:alert(1)"), ("thumbnail", "ftp://example.com/image.png"),
            ("thumbnail", "not-a-url"),
        ):
            with self.subTest(field=field, value=value):
                before = self.database_snapshot()
                response = self.client.post(self.list_url, {**self.payload, field: value}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
                self.assertEqual(self.database_snapshot(), before)

    def test_invalid_patch_does_not_partially_save_valid_fields(self):
        self.client.force_authenticate(user=self.editor)
        before = self.database_snapshot()
        response = self.client.patch(self.detail_url, {
            "title": "Valid change", "description": "<b></b>",
        }, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.database_snapshot(), before)

    def test_optional_thumbnail_accepts_blank_or_null(self):
        self.client.force_authenticate(user=self.owner)
        for value in ("", None):
            response = self.client.patch(self.detail_url, {"thumbnail": value}, format="json")
            self.assertEqual(response.status_code, 200)
            self.experience.refresh_from_db()
            self.assertEqual(self.experience.thumbnail, "")

    def test_computed_and_system_fields_cannot_be_forged_on_create_or_update(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        forged = {
            "id": forged_id, "star_count": 500, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.regular.pk],
            "started_at": "2000-01-01T00:00:00Z", "ended_at": "2001-01-01T00:00:00Z",
            "is_ongoing": False, "category_display": "forged",
        }
        response = self.client.post(self.list_url, {**self.payload, **forged}, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged_id)
        saved = Experience.objects.get(pk=response.data["id"])
        self.assertEqual(saved.starred_by.count(), 0)
        self.assertIsNone(saved.ended_at)
        self.assertGreater(saved.started_at.year, 2000)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        before = self.database_snapshot()
        response = self.client.patch(self.detail_url, forged, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.database_snapshot(), before)

    def test_unknown_resources_return_404_for_read_update_delete_and_star(self):
        self.client.force_authenticate(user=self.owner)
        detail_url = reverse("api:experience-detail", args=[uuid.uuid4()])
        star_url = reverse("api:experience-star", args=[uuid.uuid4()])
        before = self.database_snapshot()
        for method in ("get", "put", "patch", "delete"):
            response = getattr(self.client, method)(detail_url, {}, format="json")
            self.assertEqual(response.status_code, 404)
        self.assertEqual(self.client.post(star_url).status_code, 404)
        self.assertEqual(self.database_snapshot(), before)

    def test_wrong_methods_are_rejected_without_mutation(self):
        self.client.force_authenticate(user=self.owner)
        before = self.database_snapshot()
        for method, url in (("delete", self.list_url), ("post", self.detail_url), ("get", self.star_url)):
            self.assertEqual(getattr(self.client, method)(url).status_code, 405)
        self.assertEqual(self.database_snapshot(), before)

    def test_guest_cannot_star_and_membership_is_unchanged(self):
        before = self.database_snapshot()
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertEqual(self.database_snapshot(), before)

    def test_each_authenticated_role_can_star_unstar_and_cannot_impersonate(self):
        for user in (self.regular, self.editor, self.owner):
            with self.subTest(user=user):
                self.client.force_authenticate(user=user)
                response = self.client.post(self.star_url, {"user_id": self.staff.pk}, format="json")
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 1)
                self.assertEqual(list(self.experience.starred_by.all()), [user])
                response = self.client.post(self.star_url)
                self.assertFalse(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 0)
                self.assertFalse(self.experience.starred_by.exists())

    def test_star_does_not_remove_another_accounts_star(self):
        self.experience.starred_by.add(self.owner)
        self.client.force_authenticate(user=self.regular)
        self.assertEqual(self.client.post(self.star_url).data["star_count"], 2)
        self.assertEqual(self.client.post(self.star_url).data["star_count"], 1)
        self.assertEqual(list(self.experience.starred_by.all()), [self.owner])

    def test_list_uses_constant_queries_instead_of_one_query_per_card(self):
        for index in range(8):
            experience = Experience.objects.create(title=f"Experience {index}", description="Content")
            experience.starred_by.add(self.regular, self.owner)
        with self.assertNumQueries(2):
            response = self.client.get(self.list_url)
            self.assertEqual(len(response.data), 9)
            self.assertEqual(sum(item["star_count"] for item in response.data), 16)

    def test_real_session_rejects_missing_or_wrong_csrf_for_every_mutation(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=self.owner.username, password="test-password"))
        client.get(reverse("main:show_experience"))
        for token in (None, "x" * 32):
            headers = {"HTTP_X_CSRFTOKEN": token} if token else {}
            for method, url in (
                ("post", self.list_url), ("put", self.detail_url),
                ("patch", self.detail_url), ("delete", self.detail_url), ("post", self.star_url),
            ):
                with self.subTest(method=method, token=token):
                    before = self.database_snapshot()
                    response = getattr(client, method)(url, self.payload, format="json", **headers)
                    self.assertEqual(response.status_code, 403)
                    self.assertIn("CSRF", str(response.data))
                    self.assertEqual(self.database_snapshot(), before)

    def test_real_session_accepts_correct_csrf_for_every_mutation(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username=self.owner.username, password="test-password"))
        client.get(reverse("main:show_experience"))
        headers = {"HTTP_X_CSRFTOKEN": client.cookies["csrftoken"].value}
        self.assertEqual(client.post(self.list_url, self.payload, format="json", **headers).status_code, 201)
        self.assertEqual(client.put(self.detail_url, self.payload, format="json", **headers).status_code, 200)
        self.assertEqual(client.patch(self.detail_url, {"title": "Updated"}, format="json", **headers).status_code, 200)
        self.assertTrue(client.post(self.star_url, **headers).data["is_starred"])
        self.assertEqual(client.delete(self.detail_url, **headers).status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_regular_and_editor_pages_also_set_csrf_cookie_for_star(self):
        for user in (self.regular, self.editor):
            client = APIClient(enforce_csrf_checks=True)
            self.assertTrue(client.login(username=user.username, password="test-password"))
            self.assertEqual(client.get(reverse("main:show_experience")).status_code, 200)
            self.assertIn("csrftoken", client.cookies)
            token = client.cookies["csrftoken"].value
            self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_browsable_api_and_tutorial_projects_remain_accessible(self):
        for url in (self.list_url, self.detail_url, reverse("api:project-list")):
            response = self.client.get(url, HTTP_ACCEPT="text/html")
            self.assertEqual(response.status_code, 200)
            self.assertIn("text/html", response["Content-Type"])
            self.assertContains(response, "rest_framework")
        self.assertContains(self.client.get(reverse("main:show_projects")), reverse("api:project-list"))

    def test_page_uses_drf_endpoints_and_modals_follow_roles_without_duplicate_ids(self):
        for user, can_edit, can_create in (
            (None, False, False), (self.regular, False, False),
            (self.editor, True, False), (self.owner, True, True),
        ):
            self.client.force_login(user) if user else self.client.logout()
            page = self.client.get(reverse("main:show_experience"))
            self.assertContains(page, f'data-list-url="{self.list_url}"')
            self.assertContains(page, 'id="experience-category-filter"')
            self.assertContains(page, 'id="experience-status-filter"')
            html = page.content.decode()
            self.assertEqual('id="edit-experience-modal"' in html, can_edit)
            self.assertEqual('id="add-experience-modal"' in html, can_create)
            ids = re.findall(r'\bid="([^"]+)"', html)
            self.assertEqual(len(ids), len(set(ids)))
