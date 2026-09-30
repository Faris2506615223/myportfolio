from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms import ModelForm, Select, Textarea, TextInput, URLInput
from django.utils.html import strip_tags

from main.models import Experience, Project


class SanitizedTextModelForm(ModelForm):
    """Provide consistent server-side HTML stripping for text inputs."""

    def clean_required_text(self, field_name, label):
        value = strip_tags(self.cleaned_data[field_name]).strip()
        if not value:
            raise ValidationError(
                f"{label} tidak boleh kosong atau hanya berisi tag HTML."
            )
        return value


class ExperienceForm(SanitizedTextModelForm):
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

    def clean_title(self):
        return self.clean_required_text("title", "Posisi atau kegiatan")

    def clean_description(self):
        return self.clean_required_text("description", "Deskripsi pengalaman")

    def clean_thumbnail(self):
        return strip_tags(self.cleaned_data.get("thumbnail") or "").strip()


class ProjectForm(SanitizedTextModelForm):
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

    def clean_title(self):
        return self.clean_required_text("title", "Nama proyek")

    def clean_category(self):
        return self.clean_required_text("category", "Kategori proyek")

    def clean_description(self):
        return self.clean_required_text("description", "Deskripsi proyek")

    def clean_thumbnail(self):
        thumbnail = strip_tags(self.cleaned_data.get("thumbnail") or "").strip()
        if not thumbnail:
            return thumbnail

        if thumbnail.startswith(("/static/", "/media/")):
            return thumbnail

        try:
            URLValidator(schemes=["http", "https"])(thumbnail)
        except ValidationError as error:
            raise ValidationError(
                "Thumbnail harus berupa URL HTTP(S) atau path /static/ dan /media/."
            ) from error
        return thumbnail
