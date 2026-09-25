from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.forms import ExperienceForm
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

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_projects")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

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

    def test_projects_page_displays_data(self):
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title)
        self.assertContains(response, self.project.category)
        self.assertContains(response, self.project.description)
        self.assertContains(response, self.project.thumbnail)
        self.assertContains(response, self.project.project_url)
        self.assertContains(response, f'href="{reverse("main:show_project_detail", args=[self.project.id])}"')

    def test_empty_projects_page(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("main:show_projects"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Belum ada proyek yang ditambahkan.")

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

        self.assertContains(response, "BPJSight")
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
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Mendampingi mahasiswa saat tutorial Django.",
            category="part-time",
            thumbnail="https://example.com/asdos.jpg",
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
        self.assertEqual(payload[0]["model"], "main.experience")
        self.assertEqual(payload[0]["fields"]["title"], "Volunteer Mentor")

    def test_experience_page_displays_deserialized_json_data(self):
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
        self.assertContains(response, self.experience.title)
        self.assertNotContains(response, "Volunteer Mentor")
        self.assertIsInstance(response.context["experience_list"][0], Experience)


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
        response = self.client.get(reverse("main:create_project"))
        self.assertEqual(response.status_code, 403)

    def test_regular_user_forbidden_from_delete_project(self):
        self.client.login(username="student_pbp", password="studentpassword123")
        response = self.client.post(reverse("main:delete_project", args=[self.project.id]))
        self.assertEqual(response.status_code, 403)

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

