from django.contrib import admin
from .models import InfoPost, InfoComment, InfoTag, InfoCategory

admin.site.register(InfoPost)
admin.site.register(InfoComment)
admin.site.register(InfoTag)
admin.site.register(InfoCategory)

