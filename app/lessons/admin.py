from django.contrib import admin
from .models import Lesson, LessonSpeech

class LessonSpeechInline(admin.TabularInline): 
    model = LessonSpeech
    extra = 1


# Админ-класс для Lesson
class LessonAdm(admin.ModelAdmin):
    list_display = ('__str__', 'description')
    inlines = [LessonSpeechInline]


# Регистрация моделей в админ-панели
admin.site.register(Lesson, LessonAdm)
admin.site.register(LessonSpeech)
