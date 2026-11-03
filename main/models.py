import uuid
from django.contrib.auth.models import User
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ("internship", "Internship"),
        ("research", "Research"),
        ("volunteer", "Volunteer"),
        ("part-time", "Part-Time"),
        ("full-time", "Full-Time"),
        ("freelance", "Freelance"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=EXPERIENCE_CHOICES,
        default="full-time",
    )
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_experiences", blank=True
    )

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None

    class Meta:
        verbose_name = "Experience"
        verbose_name_plural = "Experiences"
        ordering = ["-started_at"]


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=150)
    description = models.TextField()
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    project_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __init__(self, *args, **kwargs):
        if "tech_stack" in kwargs and "category" not in kwargs:
            kwargs["category"] = kwargs.pop("tech_stack")
        if "project_image_url" in kwargs and "thumbnail" not in kwargs:
            kwargs["thumbnail"] = kwargs.pop("project_image_url")
        super().__init__(*args, **kwargs)

    @property
    def tech_stack(self):
        return self.category

    @tech_stack.setter
    def tech_stack(self, value):
        self.category = value

    @property
    def project_image_url(self):
        return self.thumbnail

    @project_image_url.setter
    def project_image_url(self, value):
        self.thumbnail = value

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ["-created_at"]
