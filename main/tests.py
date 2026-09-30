from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import Group, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.project = Project.objects.create(
            title="SimKopDes 2.0",
            category="Web App • Dashboard",
            description="Sistem informasi manajemen koperasi desa berbasis web.",
            thumbnail="/static/img/projects/Simkopdes2.0.webp",
            project_url="https://github.com/Faris2506615223",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page_renders_ajax_skeleton(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'id="experience-search-form"')
        self.assertContains(response, 'id="experience-loading"')
        self.assertContains(response, 'id="experience-error"')
        self.assertContains(response, 'id="experience-empty"')
        self.assertContains(response, 'id="experience-grid"')
        self.assertContains(response, reverse("main:get_experiences_json"))
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_empty_experience_json(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertEqual(response.json(), [])

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experiences_json"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertFalse(response.json()[0]["fields"]["is_ongoing"])

    def test_project_model(self):
        self.assertEqual(str(self.project), "SimKopDes 2.0")
        self.assertEqual(self.project.category, "Web App • Dashboard")
        self.assertEqual(self.project.thumbnail, "/static/img/projects/Simkopdes2.0.webp")

    def test_projects_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects.html")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_projects_page_renders_ajax_skeleton(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="project-search-form"')
        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, reverse("main:get_projects_json"))
        self.assertNotContains(response, self.project.title)

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Belum ada proyek yang ditambahkan atau ditemukan.",
        )

    def test_project_detail_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_project_detail", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project_detail.html")
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.category)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.project_url)
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_project_detail_nonexistent_returns_404(self):
        import uuid
        random_uuid = uuid.uuid4()
        response = self.client.get(reverse("main:show_project_detail", args=[random_uuid]))

        self.assertEqual(response.status_code, 404)

class Tutorial3Test(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin_test",
            password="adminpassword123",
        )
        self.project = Project.objects.create(
            title="BPJSight",
            category="Web Portal • Healthcare",
            description="Portal layanan administrasi kesehatan.",
            thumbnail="/static/img/projects/BPJSight.webp",
            project_url="https://github.com/Faris2506615223",
        )

    def test_create_project_page(self):
        self.client.login(username="admin_test", password="adminpassword123")
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Tambah Project")

    def test_create_project_with_valid_data(self):
        self.client.login(username="admin_test", password="adminpassword123")
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "GarudaHacks",
                "category": "Web App • Hackathon",
                "description": "Project untuk kompetisi Garuda Hacks.",
                "thumbnail": "/static/img/projects/GarudaHacks.webp",
                "project_url": "https://github.com/Faris2506615223",
            },
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertTrue(Project.objects.filter(title="GarudaHacks").exists())

    def test_create_project_rejects_invalid_data(self):
        self.client.login(username="admin_test", password="adminpassword123")
        response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "",
                "category": "Web App",
                "description": "Deskripsi tetap diisi.",
                "thumbnail": "",
                "project_url": "bukan-url-valid",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Project.objects.filter(description="Deskripsi tetap diisi.").exists())
        self.assertContains(response, "This field is required")
        self.assertContains(response, "Enter a valid URL")

    def test_projects_json_endpoint_and_title_filter(self):
        Project.objects.create(
            title="PressPoint",
            category="3D Model",
            description="Platform pemetaan titik tekanan.",
        )

        response = self.client.get(
            reverse("main:get_projects_json"),
            {"title": "press"},
        )
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["fields"]["title"], "PressPoint")

    def test_projects_page_search(self):
        Project.objects.create(
            title="PressPoint",
            category="3D Model",
            description="Platform pemetaan titik tekanan.",
        )

        response = self.client.get(
            reverse("main:show_projects"),
            {"title": "BPJ"},
        )

        self.assertContains(response, 'value="BPJ"')
        self.assertNotContains(response, "BPJSight")
        self.assertNotContains(response, "PressPoint")

    def test_delete_project_rejects_get_request(self):
        self.client.login(username="admin_test", password="adminpassword123")
        response = self.client.get(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_with_post_request(self):
        self.client.login(username="admin_test", password="adminpassword123")
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())


class ExperienceManagementTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="experience_admin",
            password="experiencepassword123",
        )
        self.regular_user = User.objects.create_user(
            username="experience_viewer",
            password="viewerpassword123",
        )
        self.client.login(
            username="experience_admin",
            password="experiencepassword123",
        )
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Mendampingi mahasiswa saat tutorial Django.",
            category="part-time",
            thumbnail="https://example.com/asdos.jpg",
        )

    def test_anonymous_user_redirected_from_experience_mutations(self):
        self.client.logout()

        create_response = self.client.get(reverse("main:create_experience"))
        update_response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )
        delete_response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertRedirects(
            create_response,
            f"/login/?next={reverse('main:create_experience')}",
        )
        self.assertRedirects(
            update_response,
            f"/login/?next={reverse('main:update_experience', args=[self.experience.id])}",
        )
        self.assertRedirects(
            delete_response,
            f"/login/?next={reverse('main:delete_experience', args=[self.experience.id])}",
        )
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_regular_user_forbidden_from_experience_mutations(self):
        self.client.logout()
        self.client.login(
            username="experience_viewer",
            password="viewerpassword123",
        )

        create_response = self.client.get(reverse("main:create_experience"))
        update_response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )
        create_post_response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Unauthorized Experience",
                "description": "Data ini tidak boleh tersimpan.",
                "category": "internship",
                "thumbnail": "",
            },
        )
        update_post_response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Unauthorized Update",
                "description": "Data ini tidak boleh berubah.",
                "category": "research",
                "thumbnail": "",
            },
        )
        delete_response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(create_post_response.status_code, 403)
        self.assertEqual(update_post_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())
        self.assertFalse(
            Experience.objects.filter(title="Unauthorized Experience").exists()
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Asisten Dosen PBP")

    def test_regular_user_does_not_see_experience_crud_controls(self):
        self.client.logout()
        self.client.login(
            username="experience_viewer",
            password="viewerpassword123",
        )

        response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(response, reverse("main:create_experience"))
        self.assertNotContains(
            response,
            reverse("main:update_experience", args=[self.experience.id]),
        )
        self.assertNotContains(
            response,
            reverse("main:delete_experience", args=[self.experience.id]),
        )

    def test_experience_form_contains_only_editable_data_fields(self):
        self.assertEqual(
            list(ExperienceForm.base_fields),
            ["title", "description", "category", "thumbnail"],
        )

    def test_create_experience_page_extends_base_template(self):
        response = self.client.get(reverse("main:create_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Tambah Experience")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_experience_with_valid_data(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Software Engineer Intern",
                "description": "Mengembangkan fitur aplikasi web internal.",
                "category": "internship",
                "thumbnail": "https://example.com/internship.jpg",
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(
            Experience.objects.filter(title="Software Engineer Intern").exists()
        )

    def test_create_experience_rejects_invalid_data(self):
        response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "",
                "description": "Deskripsi tetap diisi.",
                "category": "kategori-tidak-valid",
                "thumbnail": "bukan-url-valid",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Experience.objects.filter(description="Deskripsi tetap diisi.").exists()
        )
        self.assertContains(response, "This field is required")
        self.assertContains(response, "Select a valid choice")
        self.assertContains(response, "Enter a valid URL")

    def test_update_experience_page_is_prefilled(self):
        response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertContains(response, "Ubah Experience")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)

    def test_update_experience_with_valid_data(self):
        response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Teaching Assistant PBP",
                "description": "Mendampingi tutorial dan memberikan umpan balik.",
                "category": "part-time",
                "thumbnail": "https://example.com/teaching-assistant.jpg",
            },
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Teaching Assistant PBP")
        self.assertEqual(Experience.objects.count(), 1)

    def test_delete_experience_rejects_get_request(self):
        response = self.client.get(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Experience.objects.filter(pk=self.experience.id).exists())

    def test_delete_experience_with_post_request(self):
        response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_experiences_json_endpoint_and_title_filter(self):
        Experience.objects.create(
            title="Volunteer Mentor",
            description="Mengajar pemrograman dasar.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:get_experiences_json"),
            {"title": "mentor"},
        )
        payload = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["fields"]["title"], "Volunteer Mentor")
        self.assertEqual(payload[0]["fields"]["category_display"], "Volunteer")

    def test_experience_page_only_renders_skeleton_and_preserves_query(self):
        Experience.objects.create(
            title="Volunteer Mentor",
            description="Mengajar pemrograman dasar.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:show_experience"),
            {"title": "Asisten"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'value="Asisten"')
        self.assertContains(response, 'id="experience-grid"')
        self.assertNotContains(response, '<article class="experience-card">')
        self.assertNotContains(response, "Volunteer Mentor")


class Assignment4Test(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="portfolio_owner",
            password="ownerpassword123",
        )
        self.regular_user = User.objects.create_user(
            username="portfolio_reader",
            password="readerpassword123",
        )
        self.editor = User.objects.create_user(
            username="portfolio_editor",
            password="editorpassword123",
        )
        self.editor_group, self.editor_group_created = Group.objects.get_or_create(
            name="Editor"
        )
        self.editor.groups.add(self.editor_group)
        self.experience = Experience.objects.create(
            title="Software Engineer Intern",
            description="Mengembangkan fitur aplikasi internal.",
            category="internship",
            thumbnail="https://example.com/internship.jpg",
        )

    def test_editor_group_is_provisioned_by_migration(self):
        self.assertFalse(self.editor_group_created)

    def test_public_can_read_but_anonymous_mutations_redirect_to_login(self):
        list_response = self.client.get(reverse("main:show_experience"))
        api_response = self.client.get(reverse("main:get_experiences_json"))
        create_response = self.client.get(reverse("main:create_experience"))
        update_response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )
        delete_response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )
        star_response = self.client.post(
            reverse("main:toggle_experience_star", args=[self.experience.id])
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(api_response.status_code, 200)
        self.assertRedirects(
            create_response,
            f"/login/?next={reverse('main:create_experience')}",
        )
        self.assertRedirects(
            update_response,
            f"/login/?next={reverse('main:update_experience', args=[self.experience.id])}",
        )
        self.assertRedirects(
            delete_response,
            f"/login/?next={reverse('main:delete_experience', args=[self.experience.id])}",
        )
        self.assertRedirects(
            star_response,
            f"/login/?next={reverse('main:toggle_experience_star', args=[self.experience.id])}",
        )

    def test_regular_user_cannot_create_update_or_delete_experience(self):
        self.client.force_login(self.regular_user)
        create_response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Unauthorized Create",
                "description": "Tidak boleh tersimpan.",
                "category": "research",
                "thumbnail": "",
            },
        )
        update_response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Unauthorized Update",
                "description": "Tidak boleh berubah.",
                "category": "research",
                "thumbnail": "",
            },
        )
        delete_response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(update_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertFalse(
            Experience.objects.filter(title="Unauthorized Create").exists()
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineer Intern")

    def test_editor_can_update_but_cannot_create_or_delete_experience(self):
        self.client.force_login(self.editor)
        create_response = self.client.get(reverse("main:create_experience"))
        create_post_response = self.client.post(
            reverse("main:create_experience"),
            {
                "title": "Editor Cannot Create",
                "description": "Tidak boleh tersimpan.",
                "category": "research",
                "thumbnail": "",
            },
        )
        update_page_response = self.client.get(
            reverse("main:update_experience", args=[self.experience.id])
        )
        update_response = self.client.post(
            reverse("main:update_experience", args=[self.experience.id]),
            {
                "title": "Software Engineer",
                "description": "Memperbarui pengalaman sebagai editor.",
                "category": "full-time",
                "thumbnail": "https://example.com/software-engineer.jpg",
            },
        )
        delete_response = self.client.post(
            reverse("main:delete_experience", args=[self.experience.id])
        )

        self.assertEqual(create_response.status_code, 403)
        self.assertEqual(create_post_response.status_code, 403)
        self.assertEqual(update_page_response.status_code, 200)
        self.assertRedirects(update_response, reverse("main:show_experience"))
        self.assertEqual(delete_response.status_code, 403)
        self.assertFalse(
            Experience.objects.filter(title="Editor Cannot Create").exists()
        )
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Software Engineer")

    def test_experience_controls_follow_the_four_role_matrix(self):
        create_url = reverse("main:create_experience")

        anonymous_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(anonymous_response, 'data-can-edit="false"')
        self.assertContains(anonymous_response, 'data-can-delete="false"')
        self.assertNotContains(anonymous_response, create_url)
        self.assertNotContains(anonymous_response, 'id="add-experience-modal"')

        self.client.force_login(self.regular_user)
        regular_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(regular_response, "Pengguna")
        self.assertContains(regular_response, 'data-can-edit="false"')
        self.assertContains(regular_response, 'data-can-delete="false"')
        self.assertNotContains(regular_response, create_url)

        self.client.force_login(self.editor)
        editor_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(editor_response, "Editor")
        self.assertContains(editor_response, 'data-can-edit="true"')
        self.assertContains(editor_response, 'data-can-delete="false"')
        self.assertNotContains(editor_response, create_url)

        self.client.force_login(self.owner)
        owner_response = self.client.get(reverse("main:show_experience"))
        self.assertContains(owner_response, "Pemilik")
        self.assertContains(owner_response, 'data-can-edit="true"')
        self.assertContains(owner_response, 'data-can-delete="true"')
        self.assertContains(owner_response, create_url)
        self.assertContains(owner_response, 'id="add-experience-modal"')

    def test_all_authenticated_roles_can_toggle_one_experience_star(self):
        for user in (self.regular_user, self.editor, self.owner):
            self.client.force_login(user)
            response = self.client.post(
                reverse(
                    "main:toggle_experience_star",
                    args=[self.experience.id],
                )
            )
            self.assertRedirects(response, reverse("main:show_experience"))
            self.assertIn(user, self.experience.starred_by.all())

        self.assertEqual(self.experience.starred_by.count(), 3)

        self.client.force_login(self.regular_user)
        self.client.post(
            reverse(
                "main:toggle_experience_star",
                args=[self.experience.id],
            )
        )
        self.assertNotIn(self.regular_user, self.experience.starred_by.all())
        self.assertEqual(self.experience.starred_by.count(), 2)

    def test_experience_json_displays_star_count_and_user_status(self):
        star_url = reverse(
            "main:toggle_experience_star",
            args=[self.experience.id],
        )
        self.client.force_login(self.regular_user)
        self.client.post(star_url)

        starred_response = self.client.get(reverse("main:get_experiences_json"))
        starred_fields = starred_response.json()[0]["fields"]

        self.assertTrue(starred_fields["is_starred"])
        self.assertEqual(starred_fields["star_count"], 1)
        self.assertEqual(starred_fields["starred_by_names"], "portfolio_reader")

        self.client.post(star_url)
        unstarred_response = self.client.get(reverse("main:get_experiences_json"))
        unstarred_fields = unstarred_response.json()[0]["fields"]

        self.assertFalse(unstarred_fields["is_starred"])
        self.assertEqual(unstarred_fields["star_count"], 0)

    def test_experience_star_requires_post_and_csrf(self):
        star_url = reverse(
            "main:toggle_experience_star",
            args=[self.experience.id],
        )
        self.client.force_login(self.regular_user)
        get_response = self.client.get(star_url)
        page_response = self.client.get(reverse("main:show_experience"))

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.regular_user)
        missing_token_response = csrf_client.post(star_url)

        self.assertEqual(get_response.status_code, 405)
        self.assertContains(page_response, "csrfmiddlewaretoken")
        self.assertEqual(missing_token_response.status_code, 403)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_experience_json_uses_usernames_instead_of_internal_user_ids(self):
        self.experience.starred_by.add(self.regular_user, self.editor)

        response = self.client.get(reverse("main:get_experiences_json"))
        payload = response.json()
        serialized_experience = next(
            item for item in payload if item["pk"] == str(self.experience.id)
        )

        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            serialized_experience["fields"]["starred_by"],
            [["portfolio_reader"], ["portfolio_editor"]],
        )


class Tutorial4Test(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="admin_pbp",
            password="adminpassword123",
        )
        self.regular_user = User.objects.create_user(
            username="student_pbp",
            password="studentpassword123",
        )
        self.project = Project.objects.create(
            title="Katalog Buku Fasilkom",
            category="Web App",
            description="Aplikasi web katalog buku.",
        )

    def test_anonymous_user_redirected_from_create_project(self):
        response = self.client.get(reverse("main:create_project"))
        self.assertRedirects(response, f"/login/?next={reverse('main:create_project')}")

    def test_anonymous_user_redirected_from_delete_project(self):
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertRedirects(response, f"/login/?next={reverse('main:delete_project', args=[self.project.id])}")

    def test_regular_user_forbidden_from_create_project(self):
        self.client.login(username="student_pbp", password="studentpassword123")
        get_response = self.client.get(reverse("main:create_project"))
        post_response = self.client.post(
            reverse("main:create_project"),
            {
                "title": "Unauthorized Project",
                "category": "Web App",
                "description": "Data ini tidak boleh tersimpan.",
                "thumbnail": "",
                "project_url": "",
            },
        )

        self.assertEqual(get_response.status_code, 403)
        self.assertEqual(post_response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Unauthorized Project").exists())

    def test_regular_user_forbidden_from_delete_project(self):
        self.client.login(username="student_pbp", password="studentpassword123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_regular_user_sees_star_but_not_project_crud_controls(self):
        self.client.login(username="student_pbp", password="studentpassword123")

        response = self.client.get(reverse("main:show_projects"))

        self.assertContains(response, "const starUrl")
        self.assertContains(response, 'const IS_SUPERUSER = "false"')
        self.assertNotContains(response, 'id="add-project-modal"')
        self.assertNotContains(response, reverse("main:create_project"))
        self.assertNotContains(
            response,
            reverse("main:delete_project", args=[self.project.id]),
        )

    def test_register_page_renders_and_creates_account(self):
        get_response = self.client.get(reverse("main:register"))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "register.html")

        post_response = self.client.post(
            reverse("main:register"),
            {
                "username": "newuser123",
                "password1": "ComplexPassword!987",
                "password2": "ComplexPassword!987",
            },
        )
        self.assertRedirects(post_response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="newuser123").exists())

    def test_login_user_sets_last_login_cookie(self):
        get_response = self.client.get(reverse("main:login"))
        self.assertEqual(get_response.status_code, 200)
        self.assertTemplateUsed(get_response, "login.html")

        post_response = self.client.post(
            reverse("main:login"),
            {
                "username": "student_pbp",
                "password": "studentpassword123",
            },
        )
        self.assertRedirects(post_response, reverse("main:show_main"))
        self.assertIn("last_login", post_response.cookies)

    def test_logout_user_deletes_last_login_cookie(self):
        self.client.login(username="student_pbp", password="studentpassword123")
        response = self.client.get(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_show_main_reads_last_login_cookie(self):
        self.client.cookies["last_login"] = "2026-09-22 10:00:00"
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2026-09-22 10:00:00")

    def test_toggle_star_functionality(self):
        # Anonymous user cannot star
        anon_response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertRedirects(anon_response, f"/login/?next={reverse('main:toggle_star', args=[self.project.id])}")

        # Regular user can star
        self.client.login(username="student_pbp", password="studentpassword123")
        star_response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertRedirects(star_response, reverse("main:show_projects"))
        self.assertEqual(self.project.starred_by.count(), 1)
        self.assertIn(self.regular_user, self.project.starred_by.all())

        # Star again toggles it off (unstar)
        unstar_response = self.client.post(reverse("main:toggle_star", args=[self.project.id]))
        self.assertRedirects(unstar_response, reverse("main:show_projects"))
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_get_projects_json_uses_natural_foreign_keys(self):
        self.project.starred_by.add(self.regular_user)
        response = self.client.get(reverse("main:get_projects_json"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        target_project = next(p for p in data if p["pk"] == str(self.project.id))
        self.assertEqual(target_project["fields"]["starred_by"], [["student_pbp"]])


class Tutorial5Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="tutorial5_owner",
            password="ownerpassword123",
        )
        cls.regular_user = User.objects.create_user(
            username="tutorial5_reader",
            password="readerpassword123",
        )
        cls.project = Project.objects.create(
            title="Interactive Portfolio",
            category="Django & JavaScript",
            description="Proyek yang dimuat melalui Fetch API.",
            thumbnail="/static/img/projects/BPJSight.webp",
            project_url="https://example.com/project",
        )

    def valid_project_data(self, **overrides):
        data = {
            "title": "Project AJAX",
            "category": "Django",
            "description": "Dibuat tanpa memuat ulang halaman.",
            "thumbnail": "/static/img/projects/GarudaHacks.webp",
            "project_url": "https://example.com/ajax-project",
        }
        data.update(overrides)
        return data

    def test_projects_json_contains_star_metadata_for_current_user(self):
        self.project.starred_by.add(self.regular_user)
        self.client.force_login(self.regular_user)

        response = self.client.get(reverse("main:get_projects_json"))
        payload = response.json()
        fields = next(
            item["fields"]
            for item in payload
            if item["pk"] == str(self.project.id)
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(fields["star_count"], 1)
        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["starred_by_names"], "tutorial5_reader")

    def test_ajax_create_only_accepts_post(self):
        self.client.force_login(self.owner)
        response = self.client.get(reverse("main:create_project_ajax"))

        self.assertEqual(response.status_code, 405)

    def test_ajax_create_returns_json_403_without_owner_access(self):
        endpoint = reverse("main:create_project_ajax")

        anonymous_response = self.client.post(
            endpoint,
            self.valid_project_data(),
        )
        self.client.force_login(self.regular_user)
        regular_response = self.client.post(
            endpoint,
            self.valid_project_data(),
        )

        self.assertEqual(anonymous_response.status_code, 403)
        self.assertEqual(regular_response.status_code, 403)
        self.assertIn("message", anonymous_response.json())
        self.assertFalse(Project.objects.filter(title="Project AJAX").exists())

    def test_ajax_create_saves_valid_project_and_returns_201(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("main:create_project_ajax"),
            self.valid_project_data(
                title="Project <b>AJAX</b>",
                category="<strong>Full Stack</strong>",
                description="Aman dari <em>HTML</em> tersimpan.",
            ),
        )

        self.assertEqual(response.status_code, 201)
        project = Project.objects.get(pk=response.json()["pk"])
        self.assertEqual(project.title, "Project AJAX")
        self.assertEqual(project.category, "Full Stack")
        self.assertEqual(project.description, "Aman dari HTML tersimpan.")

    def test_ajax_create_returns_field_errors_for_invalid_input(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("main:create_project_ajax"),
            self.valid_project_data(title='<img src="x" onerror="alert(1)">'),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertFalse(
            Project.objects.filter(category="Django", title="").exists()
        )

    def test_project_form_rejects_unsafe_thumbnail_scheme(self):
        form = ProjectForm(
            data=self.valid_project_data(
                thumbnail="javascript:alert(1)",
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail", form.errors)

    def test_projects_page_contains_ajax_xss_and_debounce_guards(self):
        response = self.client.get(reverse("main:show_projects"))
        utility_source = Path(
            settings.BASE_DIR,
            "static",
            "js",
            "ajax-utils.js",
        ).read_text(encoding="utf-8")

        self.assertContains(response, "static/js/ajax-utils.js")
        self.assertIn("function escapeHtml(value)", utility_source)
        self.assertContains(response, "new AbortController()")
        self.assertContains(response, "SEARCH_DEBOUNCE_DELAY = 300")
        self.assertContains(response, "event.preventDefault()")
        self.assertContains(response, "fetchProjects(searchInput.value.trim())")

    def test_add_project_modal_is_only_rendered_for_owner(self):
        anonymous_response = self.client.get(reverse("main:show_projects"))
        self.client.force_login(self.owner)
        owner_response = self.client.get(reverse("main:show_projects"))

        self.assertNotContains(anonymous_response, 'id="add-project-modal"')
        self.assertContains(owner_response, 'id="add-project-modal"')
        self.assertContains(owner_response, 'id="project-form"')
        self.assertContains(owner_response, "csrfmiddlewaretoken")

    def test_ajax_create_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        csrf_client.get(reverse("main:show_projects"))

        missing_token_response = csrf_client.post(
            reverse("main:create_project_ajax"),
            self.valid_project_data(),
        )
        accepted_response = csrf_client.post(
            reverse("main:create_project_ajax"),
            self.valid_project_data(title="Project dengan CSRF"),
            HTTP_X_CSRFTOKEN=csrf_client.cookies["csrftoken"].value,
        )

        self.assertEqual(missing_token_response.status_code, 403)
        self.assertEqual(accepted_response.status_code, 201)


class Assignment5Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="assignment5_owner",
            password="ownerpassword123",
        )
        cls.regular_user = User.objects.create_user(
            username="assignment5_reader",
            password="readerpassword123",
        )
        cls.experience = Experience.objects.create(
            title="Teaching Assistant",
            description="Mendampingi tutorial pemrograman web.",
            category="part-time",
            thumbnail="https://example.com/teaching.jpg",
        )

    def valid_experience_data(self, **overrides):
        data = {
            "title": "Software Engineer Intern",
            "description": "Mengembangkan fitur aplikasi internal.",
            "category": "internship",
            "thumbnail": "https://example.com/internship.jpg",
        }
        data.update(overrides)
        return data

    def test_experience_json_contains_star_metadata_for_current_user(self):
        self.experience.starred_by.add(self.regular_user)
        self.client.force_login(self.regular_user)

        response = self.client.get(reverse("main:get_experiences_json"))
        fields = response.json()[0]["fields"]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(fields["star_count"], 1)
        self.assertTrue(fields["is_starred"])
        self.assertEqual(fields["starred_by_names"], "assignment5_reader")

    def test_experience_json_supports_ajax_title_search(self):
        Experience.objects.create(
            title="Volunteer Mentor",
            description="Mengajar pemrograman dasar.",
            category="volunteer",
        )

        response = self.client.get(
            reverse("main:get_experiences_json"),
            {"title": "volunteer"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["fields"]["title"], "Volunteer Mentor")

    def test_ajax_create_only_accepts_post(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("main:create_experience_ajax"))

        self.assertEqual(response.status_code, 405)

    def test_ajax_create_returns_json_403_without_owner_access(self):
        endpoint = reverse("main:create_experience_ajax")

        anonymous_response = self.client.post(
            endpoint,
            self.valid_experience_data(),
        )
        self.client.force_login(self.regular_user)
        regular_response = self.client.post(
            endpoint,
            self.valid_experience_data(),
        )

        self.assertEqual(anonymous_response.status_code, 403)
        self.assertEqual(regular_response.status_code, 403)
        self.assertIn("message", anonymous_response.json())
        self.assertFalse(
            Experience.objects.filter(title="Software Engineer Intern").exists()
        )

    def test_ajax_create_sanitizes_text_and_returns_201(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            self.valid_experience_data(
                title="Software <b>Engineer</b> Intern",
                description="Membangun <em>fitur aman</em>.",
            ),
        )

        self.assertEqual(response.status_code, 201)
        experience = Experience.objects.get(pk=response.json()["pk"])
        self.assertEqual(experience.title, "Software Engineer Intern")
        self.assertEqual(experience.description, "Membangun fitur aman.")

    def test_ajax_create_returns_validation_errors_for_xss_payload(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("main:create_experience_ajax"),
            self.valid_experience_data(
                title='<img src="x" onerror="alert(1)">',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_experience_form_rejects_unsafe_thumbnail_scheme(self):
        form = ExperienceForm(
            data=self.valid_experience_data(thumbnail="javascript:alert(1)")
        )

        self.assertFalse(form.is_valid())
        self.assertIn("thumbnail", form.errors)

    def test_experience_page_loads_ajax_module_and_all_states(self):
        response = self.client.get(reverse("main:show_experience"))
        script_source = Path(
            settings.BASE_DIR,
            "static",
            "js",
            "experience.js",
        ).read_text(encoding="utf-8")

        self.assertContains(response, "static/js/experience.js")
        self.assertContains(response, 'id="experience-loading"')
        self.assertContains(response, 'id="experience-error"')
        self.assertContains(response, 'id="experience-empty"')
        self.assertIn("new AbortController()", script_source)
        self.assertIn("SEARCH_DEBOUNCE_DELAY = 300", script_source)
        self.assertIn("event.preventDefault()", script_source)
        self.assertIn("fetchExperiences(searchInput.value.trim())", script_source)
        self.assertIn("textContent", script_source)
        self.assertNotIn("innerHTML", script_source)

    def test_add_experience_modal_is_only_rendered_for_owner(self):
        anonymous_response = self.client.get(reverse("main:show_experience"))
        self.client.force_login(self.owner)
        owner_response = self.client.get(reverse("main:show_experience"))

        self.assertNotContains(anonymous_response, 'id="add-experience-modal"')
        self.assertContains(owner_response, 'id="add-experience-modal"')
        self.assertContains(owner_response, 'id="experience-form"')
        self.assertContains(owner_response, "csrfmiddlewaretoken")

    def test_ajax_create_requires_csrf_token(self):
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        csrf_client.get(reverse("main:show_experience"))

        missing_token_response = csrf_client.post(
            reverse("main:create_experience_ajax"),
            self.valid_experience_data(),
        )
        accepted_response = csrf_client.post(
            reverse("main:create_experience_ajax"),
            self.valid_experience_data(title="Experience dengan CSRF"),
            HTTP_X_CSRFTOKEN=csrf_client.cookies["csrftoken"].value,
        )

        self.assertEqual(missing_token_response.status_code, 403)
        self.assertEqual(accepted_response.status_code, 201)

