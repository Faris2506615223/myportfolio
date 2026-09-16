from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm
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
    json_response = get_experiences_json(request)
    deserialized_experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [item.object for item in deserialized_experiences]

    context = {
        "name": "Faris",
        "experience_list": experiences,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "experience.html", context)


def create_experience(request):
    if request.method == "POST":
        form = ExperienceForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Pengalaman baru berhasil ditambahkan.")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm()

    context = {
        "name": "Faris",
        "form": form,
        "form_title": "Tambah Experience",
        "form_kicker": "Tambahkan perjalanan baru",
        "submit_label": "Tambah Experience",
    }
    return render(request, "experience_form.html", context)


def update_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)

    if request.method == "POST":
        form = ExperienceForm(request.POST, instance=experience)

        if form.is_valid():
            form.save()
            messages.success(request, "Pengalaman berhasil diperbarui.")
            return redirect("main:show_experience")
    else:
        form = ExperienceForm(instance=experience)

    context = {
        "name": "Faris",
        "form": form,
        "form_title": "Ubah Experience",
        "form_kicker": "Perbarui detail perjalanan",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experience_form.html", context)


@require_POST
def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus.")
    return redirect("main:show_experience")


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def show_projects(request):
    json_response = get_projects_json(request)
    deserialized_projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [item.object for item in deserialized_projects]

    context = {
        "name": "Faris",
        "project_list": projects,
        "title_query": request.GET.get("title", "").strip(),
    }
    return render(request, "projects.html", context)


def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan.")
            return redirect("main:show_projects")
    else:
        form = ProjectForm()

    context = {
        "name": "Faris",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def show_project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    context = {
        "name": "Faris",
        "project": project,
    }
    return render(request, "project_detail.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_xml = serializers.serialize("xml", projects)
    return HttpResponse(projects_xml, content_type="application/xml")


@require_POST
def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    messages.success(request, "Project berhasil dihapus.")
    return redirect("main:show_projects")
