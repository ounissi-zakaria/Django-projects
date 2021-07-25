from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:topic_id>/comment", views.comment, name="comment"),
]
