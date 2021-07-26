from django import forms


class TextForm(forms.Form):
    body = forms.CharField(label="Text :", widget=forms.Textarea)
