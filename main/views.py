from django.shortcuts import get_object_or_404, render

from main.models import Experience, Project


def show_main(request):
    context = {
        "name": "Faris",
        "npm": "2506615223",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Faris",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_projects(request):
    context = {
        "name": "Faris",
        "project_list": Project.objects.all(),
    }
    return render(request, "projects.html", context)


def show_project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    context = {
        "name": "Faris",
        "project": project,
    }
    return render(request, "project_detail.html", context)
