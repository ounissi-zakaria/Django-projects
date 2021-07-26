from django.db import models
import hashlib
import string


class Text(models.Model):
    text_body = models.TextField()
    text_url = models.SlugField(max_length=10)
    text_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_body

    def generate_url(self):
        letters = string.ascii_letters + string.digits
        hash = int(hashlib.sha256(self.text_body.encode("utf-8")).hexdigest(), 16)
        url = ""
        for i in range(10):
            url += letters[hash % len(letters)]
            hash = hash // len(letters)
        return url
