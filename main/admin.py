from django.contrib import admin
from .models import NoteActive, NoteInactive, User, Topic, Color, SiteLinks

# Register your models here.
admin.site.register(NoteActive)
admin.site.register(NoteInactive)
admin.site.register(Topic)
admin.site.register(Color)
admin.site.register(User)
admin.site.register(SiteLinks)
