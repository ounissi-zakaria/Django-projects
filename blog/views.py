from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic, View
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse

from .models import Topic, Comment
from .forms import CommentForm


class IndexView(generic.ListView):
    template_name = "blog/index.html"

    def get_queryset(self):
        return Topic.objects.filter(topic_date__lte=timezone.now()).order_by(
            "-topic_date"
        )


class DetailView(View):
    def get(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id, topic_date__lte=timezone.now())
        form = CommentForm()
        context = {"topic": topic, "form": form}
        return render(request, "blog/detail.html", context)

    def post(self, request, topic_id):
        topic = get_object_or_404(Topic, pk=topic_id, topic_date__lte=timezone.now())
        form = CommentForm(request.POST)
        if form.is_valid():
            topic.comment_set.create(
                comment_user=form.cleaned_data["user"],
                comment_body=form.cleaned_data["body"],
            )
            return HttpResponseRedirect(reverse("blog:detail", args=(topic_id,)))
        return HttpResponse(status = 400)
