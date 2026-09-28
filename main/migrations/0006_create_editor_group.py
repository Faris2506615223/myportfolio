from django.db import migrations


EDITOR_GROUP_NAME = "Editor"


def create_editor_group(apps, schema_editor):
    group_model = apps.get_model("auth", "Group")
    group_model.objects.get_or_create(name=EDITOR_GROUP_NAME)


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("main", "0005_experience_starred_by"),
    ]

    operations = [
        migrations.RunPython(
            create_editor_group,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
