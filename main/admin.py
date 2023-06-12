from django.contrib import admin

from register.models import ColorPreference
from .models import NoteActive, NoteInactive, User, Topic, Color, SiteLinks


class ColorPreferenceAdmin(admin.ModelAdmin):
    list_display = ("high_importance", "medium_importance", "low_importance")
    exclude = ('slug',)


# Register your models here.
admin.site.register(NoteActive)
admin.site.register(NoteInactive)
admin.site.register(Topic)
admin.site.register(Color)
admin.site.register(User)
admin.site.register(SiteLinks)
admin.site.register(ColorPreference, ColorPreferenceAdmin)
