from django.contrib import admin
from .models import Lesson

class LessonAdm(admin.ModelAdmin):
    list_display = ('__str__', 'description')

admin.site.register(Lesson, LessonAdm)
