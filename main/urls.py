from django.urls import path

from main.views import (
    create_experience,
    create_project,
    delete_experience,
    delete_project,
    get_experiences_json,
    get_projects_json,
    get_projects_xml,
    login_user,
    logout_user,
    register,
    show_experience,
    show_main,
    show_project_detail,
    show_projects,
    toggle_star,
    update_experience,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path(
        "experience/<uuid:id>/edit/",
        update_experience,
        name="update_experience",
    ),
    path(
        "experience/<uuid:id>/delete/",
        delete_experience,
        name="delete_experience",
    ),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),
    path("projects/<uuid:id>/delete/", delete_project, name="delete_project"),
    path("projects/<uuid:id>/", show_project_detail, name="show_project_detail"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/projects/xml/", get_projects_xml, name="get_projects_xml"),
]
