from django.contrib import admin
from .models import DiscussionPost, DiscussionCategory, Comment

admin.site.register(DiscussionPost)
admin.site.register(DiscussionCategory)
admin.site.register(Comment)
