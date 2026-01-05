from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path("ping/", views.ping, name="ping"),
    path("accounts/register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
]
