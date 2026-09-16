from django.forms import ModelForm, Select, Textarea, TextInput, URLInput

from main.models import Experience, Project


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
        ]
        labels = {
            "title": "Posisi / Kegiatan",
            "description": "Deskripsi Pengalaman",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Asisten Dosen PBP",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan peran dan kontribusi utama",
                    "rows": 5,
                }
            ),
            "category": Select(),
            "thumbnail": URLInput(
                attrs={
                    "placeholder": "https://example.com/gambar-pengalaman.jpg",
                }
            ),
        }


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "category",
            "description",
            "thumbnail",
            "project_url",
        ]
        labels = {
            "title": "Nama Proyek",
            "category": "Kategori / Tech Stack",
            "description": "Deskripsi Proyek",
            "thumbnail": "URL atau Path Thumbnail",
            "project_url": "URL Proyek / Repositori",
        }
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: BPJSight",
                    "maxlength": 255,
                }
            ),
            "category": TextInput(
                attrs={
                    "placeholder": "Contoh: Web Portal • Healthcare",
                    "maxlength": 150,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Jelaskan tujuan dan fitur utama proyek",
                    "rows": 5,
                }
            ),
            "thumbnail": TextInput(
                attrs={
                    "placeholder": "/static/img/projects/BPJSight.webp",
                    "maxlength": 255,
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/Faris2506615223/nama-repo",
                }
            ),
        }
