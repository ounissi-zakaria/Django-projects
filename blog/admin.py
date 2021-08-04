from django.contrib import admin
from .models import Topic, Comment



class TopicAdmin(admin.ModelAdmin):
    fields = ["topic_title", "topic_body", "topic_date"]
    list_display = ["topic_title", "topic_date", "number_of_comments"]
    search_fields = ["topic_title"]


admin.site.register(Topic, TopicAdmin)
