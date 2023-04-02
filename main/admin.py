from django.contrib import admin
from .models import Note, User, Topic, Color

# Register your models here.
admin.site.register(Note)
admin.site.register(Topic)
admin.site.register(Color)
admin.site.register(User)
