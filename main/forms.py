from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.forms import ModelForm, Select, Textarea, TextInput, URLInput
from django.utils.html import strip_tags

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

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError(
                "Nama proyek tidak boleh hanya berisi tag HTML."
            )
        return title

    def clean_category(self):
        return strip_tags(self.cleaned_data["category"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

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
