from django.contrib import admin
from .models import InformationItem, Comment, Tag

admin.site.register(InformationItem)
admin.site.register(Comment)
admin.site.register(Tag)
