from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect

from .models import Topic, Comment


class IndexView(generic.ListView):
    template_name = "blog/index.html"

    def get_queryset(self):
        return Topic.objects.filter(topic_date__lte=timezone.now()).order_by(
            "-topic_date"
        )


class DetailView(generic.DetailView):
    model = Topic
    template_name = "blog/detail.html"

    def get_queryset(self):
        return Topic.objects.filter(topic_date__lte=timezone.now())


def comment(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    topic.comment_set.create(comment_user = request.POST["user"], comment_body=request.POST["body"])
    return HttpResponseRedirect(reverse("blog:detail", args=(topic_id,)))
