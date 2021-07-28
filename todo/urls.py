from django.urls import path
from . import views

app_name = "todo"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/delete", views.TaskDeleteView.as_view(), name="delete"),
]
