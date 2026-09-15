from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

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
        self.project = Project.objects.create(
            title="BPJSight",
            category="Web Portal • Healthcare",
            description="Portal layanan administrasi kesehatan.",
            thumbnail="/static/img/projects/BPJSight.webp",
            project_url="https://github.com/Faris2506615223",
        )

    def test_create_project_page(self):
        response = self.client.get(reverse("main:create_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "projects_form.html")
        self.assertContains(response, "Tambah Project")

    def test_create_project_with_valid_data(self):
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
        response = self.client.get(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())

    def test_delete_project_with_post_request(self):
        response = self.client.post(
            reverse("main:delete_project", args=[self.project.id])
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())