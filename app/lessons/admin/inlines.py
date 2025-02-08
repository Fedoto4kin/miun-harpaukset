from django.urls import reverse
from django.utils.html import format_html
from nested_admin import NestedGenericTabularInline, NestedStackedInline
from django.contrib import admin
from ..models import LessonSpeech, Module, Exercise
from .forms import ExerciseForm, ModuleForm


class LessonSpeechNestedInline(NestedGenericTabularInline):  # Используйте NestedGenericTabularInline здесь
    model = LessonSpeech
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 0
    max_num = 1
    fields = ('code', 'mp3', 'text')

class ExerciseInline(NestedStackedInline):
    model = Exercise
    form = ExerciseForm
    extra = 0
    fields = ('exercise_type', 'data')

class ModuleInline(NestedStackedInline):
    model = Module
    form=ModuleForm
    extra = 1
    fields = ('number', 'html_content', 'tags', 'edit_link')
    inlines = [LessonSpeechNestedInline]

    readonly_fields = ('edit_link',)

    def edit_link(self, obj):
        if obj.id:
            url = reverse('admin:lessons_module_change', args=[obj.id])
            return format_html('<a href="{}">Edit</a>', url)
        return ""

    edit_link.short_description = 'Edit Link'  # Задайте описание для столбца
    edit_link.allow_tags = True  
