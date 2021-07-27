from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Task
from .forms import TaskForm


def index(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task(body=form.cleaned_data["body"])
            task.save()
        return HttpResponseRedirect("/todo/")
    form = TaskForm()
    task_list = Task.objects.all()
    context = {
        "form": form,
        "task_list": task_list,
    }
    return render(request, "todo/index.html", context)
