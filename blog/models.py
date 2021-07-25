from django.db import models


class Topic(models.Model):
    topic_title = models.CharField(max_length=200)
    topic_body = models.TextField()
    topic_date = models.DateTimeField("date published")
    def __str__(self):
        return self.topic_title
    def number_of_comments(self):
        return len(self.comment_set.all())


class Comment(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    comment_user = models.CharField(max_length=200)
    comment_body = models.TextField()
    comment_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
        return self.comment_body
