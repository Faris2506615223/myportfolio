import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


def show_main(request):
    last_login = request.COOKIES.get("last_login", "Belum ada sesi login / Cookie tidak ditemukan")
    context = {
        "name": "Faris",
        "npm": "2506615223",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
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


@login_required(login_url="/login/")
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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

    projects_json = serializers.serialize(
        "json",
        projects,
        use_natural_foreign_keys=True
    )
    return HttpResponse(projects_json, content_type="application/json")


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_xml = serializers.serialize("xml", projects)
    return HttpResponse(projects_xml, content_type="application/xml")


@require_POST
@login_required(login_url="/login/")
def delete_project(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=id)
    project.delete()
    messages.success(request, "Project berhasil dihapus.")
    return redirect("main:show_projects")


def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")
    context = {
        "name": "Faris",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie("last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return response
    context = {
        "name": "Faris",
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)
    return redirect("main:show_projects")
