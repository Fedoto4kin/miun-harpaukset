from django.contrib import admin
from .models import Lesson

class LessonAdm(admin.ModelAdmin):
    list_display = ('num', 'title', 'slogan', 'name')

    search_fields = ('title',)

admin.site.register(Lesson, LessonAdm)
