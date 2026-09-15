from django.forms import ModelForm, Textarea, TextInput, URLInput

from main.models import Project


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