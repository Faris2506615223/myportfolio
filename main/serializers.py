from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    tech_stack = serializers.CharField(source="category", max_length=150)
    project_image_url = serializers.CharField(
        source="thumbnail",
        required=False,
        allow_blank=True,
        allow_null=True,
        default="",
    )
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        read_only_fields = ["id"]

    def to_internal_value(self, data):
        if hasattr(data, "copy"):
            data = data.copy()
        elif isinstance(data, dict):
            data = dict(data)
        if "category" in data and "tech_stack" not in data:
            data["tech_stack"] = data["category"]
        if "thumbnail" in data and "project_image_url" not in data:
            data["project_image_url"] = data["thumbnail"]
        return super().to_internal_value(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # normalize null project_image_url to empty string if needed
        if ret.get("project_image_url") is None:
            ret["project_image_url"] = ""
        # also provide category and thumbnail for backwards compatibility
        ret["category"] = ret.get("tech_stack", "")
        ret["thumbnail"] = ret.get("project_image_url", "")
        return ret

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Title cannot be empty.")
        return value

    def validate_description(self, value):
        return strip_tags(value)

    def validate_tech_stack(self, value):
        return strip_tags(value)

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())
