from nested_admin import NestedModelAdmin
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from django import forms
from ..models import Lesson, LessonSpeech, Module
from .forms import LessonSpeechForm, ModuleForm
from .inlines import LessonSpeechNestedInline, ModuleInline, ExerciseInline

class LessonSpeechAdmin(admin.ModelAdmin):
    list_display = ('code', 'mp3', 'content_object_link')
    search_fields = ('code',)
    ordering = ['-code']
    form = LessonSpeechForm

    def content_object_link(self, obj):
        if obj.content_object:
            return format_html('<a href="{}">{}</a>', reverse(f'admin:lessons_{obj.content_object._meta.model_name}_change', args=(obj.content_object.id,)), str(obj.content_object))
        return "No linked object"
    content_object_link.short_description = 'Linked Object'

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'lesson' in request.GET or 'module' in request.GET:
            form.base_fields['content_type'].widget = forms.HiddenInput()
            form.base_fields['object_id'].widget = forms.HiddenInput()
        return form

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        lesson_id = request.GET.get('lesson')
        module_id = request.GET.get('module')
        if lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            initial['content_type'] = ContentType.objects.get_for_model(Lesson).id
            initial['object_id'] = lesson_id
            initial['linked_object_name'] = str(lesson)
        elif module_id:
            module = Module.objects.get(id=module_id)
            initial['content_type'] = ContentType.objects.get_for_model(Module).id
            initial['object_id'] = module_id
            initial['linked_object_name'] = str(module)
        return initial

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if 'lesson' in request.GET or 'module' in request.GET:
            initial_data = self.get_changeform_initial_data(request)
            extra_context['linked_object_name'] = initial_data.get('linked_object_name', '')
        return super().changeform_view(request, object_id, form_url, extra_context)


class ModuleAdmin(NestedModelAdmin):
    list_display = ('number', 'lesson', 'upload_sound_button')
    search_fields = ('lesson__title', 'number')
    ordering = ['lesson', 'number']
    inlines = [LessonSpeechNestedInline, ExerciseInline]
    list_filter = ('lesson', 'tags')
    form = ModuleForm

    def upload_sound_button(self, obj):
        if obj.module_speeches.exists():
            return obj.module_speeches.first().code
        url = reverse('admin:lessons_lessonspeech_add') + f'?module={obj.id}'
        return format_html('<a class="button" href="{}">+ Pagina</a>', url)

    upload_sound_button.short_description = 'Pagina'
    upload_sound_button.allow_tags = True

class LessonAdmin(NestedModelAdmin):
    list_display = ('__str__', 'description', 'upload_sound_button')
    inlines = [LessonSpeechNestedInline, ModuleInline]

    def upload_sound_button(self, obj):
        if obj.lesson_speeches.exists():
            return obj.lesson_speeches.first().code
        url = reverse('admin:lessons_lessonspeech_add') + f'?lesson={obj.id}'
        return format_html('<a class="button" href="{}">+ Pagina</a>', url)

    upload_sound_button.short_description = 'Pagina'
    upload_sound_button.allow_tags = True

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonSpeech, LessonSpeechAdmin)
admin.site.register(Module, ModuleAdmin)
