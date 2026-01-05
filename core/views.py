from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from datetime import datetime
import django


def index(request):
    """Home page view."""
    context = {
        "django_version": django.get_version(),
    }
    return render(request, "core/index.html", context)


def ping(request):
    """Simple HTMX endpoint to demonstrate partial rendering."""
    # The django-htmx middleware adds request.htmx
    request_type = "HTMX request" if request.htmx else "Regular request"

    context = {
        "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "request_type": request_type,
    }
    return render(request, "core/partials/ping.html", context)


def register(request):
    """User registration view."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:dashboard")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def dashboard(request):
    """Protected dashboard view - requires login."""
    context = {
        "user": request.user,
    }
    return render(request, "dashboard.html", context)
