from django.urls import path
from . import views

app_name = "pastebin"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:url>/", views.detail, name="detail"),
]
