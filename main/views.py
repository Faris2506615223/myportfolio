from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from main.access import experience_editor_required, portfolio_owner_required
from main.forms import ExperienceForm, ProjectForm
from main.models import Experience, Project


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan",
    )
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
    context = {
        "name": "Faris",
        "title_query": request.GET.get("title", "").strip(),
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)


@portfolio_owner_required
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


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat menambahkan "
                    "experience."
                )
            },
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {
                "message": "Experience berhasil ditambahkan.",
                "pk": str(experience.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )


@experience_editor_required
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


@portfolio_owner_required
@require_POST
def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    messages.success(request, "Pengalaman berhasil dihapus.")
    return redirect("main:show_experience")


def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []
    for experience in experiences:
        starred_users = list(experience.starred_by.all())
        data.append(
            {
                "pk": str(experience.id),
                "fields": {
                    "title": experience.title,
                    "description": experience.description,
                    "category": experience.category,
                    "category_display": experience.get_category_display(),
                    "thumbnail": experience.thumbnail,
                    "started_at": experience.started_at.isoformat(),
                    "ended_at": (
                        experience.ended_at.isoformat()
                        if experience.ended_at
                        else None
                    ),
                    "is_ongoing": experience.is_ongoing,
                    "star_count": len(starred_users),
                    "is_starred": (
                        request.user in starred_users
                        if request.user.is_authenticated
                        else False
                    ),
                    "starred_by_names": ", ".join(
                        user.username for user in starred_users
                    ),
                    "starred_by": [
                        [user.username] for user in starred_users
                    ],
                },
            }
        )

    return JsonResponse(data, safe=False)


def show_projects(request):
    context = {
        "name": "Faris",
        "title_query": request.GET.get("title", "").strip(),
        "form": ProjectForm(),
    }
    return render(request, "projects.html", context)


@portfolio_owner_required
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


@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": (
                    "Hanya pemilik portofolio yang dapat menambahkan proyek."
                )
            },
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {
                "message": "Proyek berhasil ditambahkan.",
                "pk": str(project.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )


def show_project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    context = {
        "name": "Faris",
        "project": project,
    }
    return render(request, "project_detail.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []
    for project in projects:
        starred_users = list(project.starred_by.all())
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        starred_by_names = ", ".join(
            user.username for user in starred_users
        )
        data.append(
            {
                "pk": str(project.id),
                "fields": {
                    "title": project.title,
                    "description": project.description,
                    "category": project.category,
                    "thumbnail": project.thumbnail,
                    "project_url": project.project_url,
                    "star_count": len(starred_users),
                    "is_starred": is_starred,
                    "starred_by_names": starred_by_names,
                    # Keep the Tutorial 04 representation available for
                    # clients that still consume natural user keys.
                    "starred_by": [
                        [user.username] for user in starred_users
                    ],
                },
            }
        )

    return JsonResponse(data, safe=False)


def get_projects_xml(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_xml = serializers.serialize(
        "xml",
        projects,
        use_natural_foreign_keys=True,
    )
    return HttpResponse(projects_xml, content_type="application/xml")


@portfolio_owner_required
@require_POST
def delete_project(request, id):
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
    next_url = request.POST.get("next") or request.GET.get("next") or ""
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            response = redirect(next_url)
        else:
            response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            timezone.localtime().strftime("%Y-%m-%d %H:%M:%S"),
            httponly=True,
            secure=request.is_secure(),
            samesite="Lax",
        )
        return response
    context = {
        "name": "Faris",
        "form": form,
        "next": next_url,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response


@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user in project.starred_by.all():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return redirect("main:show_projects")


@login_required(login_url="/login/")
@require_POST
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    if request.user in experience.starred_by.all():
        experience.starred_by.remove(request.user)
    else:
        experience.starred_by.add(request.user)
    return redirect("main:show_experience")
