from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic, View

from .models import Task
from .forms import TaskForm


class IndexView(View):
    def get(self, request):
        form = TaskForm()
        task_list = Task.objects.all()
        context = {
            "form": form,
            "task_list": task_list,
        }
        return render(request, "todo/index.html", context)

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task(body=form.cleaned_data["body"])
            task.save()
            return HttpResponseRedirect("/todo/")
        return HttpResponse(status=400)


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = "/todo/"
