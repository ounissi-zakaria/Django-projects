from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse

from .models import Text
from .forms import TextForm


def index(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            text = Text.objects.create(
                text_body=form.cleaned_data["body"],
            )
            text.text_url = text.generate_url()
            text.save()
            return HttpResponseRedirect(
                reverse("pastebin:detail", args=(text.text_url,))
            )
    form = TextForm()
    context = {"form": form}
    return render(request, "pastebin/index.html", context)


def detail(request, url):
    text = Text.objects.get(text_url__exact=url)
    context = {"text": text}
    return render(request, "pastebin/detail.html", context)
