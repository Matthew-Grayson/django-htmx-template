from django.shortcuts import render
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

