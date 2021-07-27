from django import forms


class TaskForm(forms.Form):
    body = forms.CharField(max_length=255, label="task: ")
