from django import forms


class CommentForm(forms.Form):
    user = forms.CharField(label="Your name: ", max_length=200)
    body = forms.CharField(label="Comment: ", widget=forms.Textarea)
