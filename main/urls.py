from django.urls import path

from main.views import (
    create_project,
    delete_project,
    get_projects_json,
    show_experience,
    show_main,
    show_project_detail,
    show_projects,
    get_projects_xml,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/<uuid:id>/delete/", delete_project,name="delete_project"),
    path("projects/<uuid:id>/", show_project_detail, name="show_project_detail"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/projects/xml/", get_projects_xml, name="get_projects_xml"),
]