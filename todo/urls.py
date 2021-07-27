from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/delete", views.delete, name="delete"),
]
