from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic, View
from django.utils import timezone
from django.urls import reverse
from django.db import IntegrityError

from .models import Text
from .forms import TextForm


# def index(request):
#     if request.method == "POST":
#


class IndexView(View):
    def get(self, request):
        form = TextForm()
        context = {"form": form}
        return render(request, "pastebin/index.html", context)

    def post(self, request):
        form = TextForm(request.POST)
        if form.is_valid():
            text = Text(
                text_body=form.cleaned_data["body"],
            )
            text.text_url = text.generate_url()
            try:
                text.save()
            except IntegrityError:
                pass
            return HttpResponseRedirect(
                reverse("pastebin:detail", args=(text.text_url,))
            )
        return HttpResponse(status=400)


class DetailView(generic.DetailView):
    model = Text
    template_name = "pastebin/detail.html"

    def get_object(self):
        return Text.objects.get(text_url__exact=self.kwargs["url"])
