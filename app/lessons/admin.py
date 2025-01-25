from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from .models import Lesson, LessonSpeech, Module

class LessonSpeechInline(GenericTabularInline):
    model = LessonSpeech
    extra = 1
    fields = ('code', 'mp3', 'text')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('number', 'html_content', 'tags')

class LessonSpeechAdmin(admin.ModelAdmin):
    list_display = ('code', 'mp3', 'content_object_link')
    search_fields = ('code',)
    ordering = ['-code']

    def content_object_link(self, obj):
        if obj.content_object:
            return format_html('<a href="{}">{}</a>',
                              reverse(f'admin:lessons_{obj.content_object._meta.model_name}_change', args=(obj.content_object.id,)),
                              str(obj.content_object))
        return "No linked object"
    content_object_link.short_description = 'Linked Object'

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        lesson_id = request.GET.get('lesson')
        module_id = request.GET.get('module')
        if lesson_id:
            initial['content_type'] = ContentType.objects.get_for_model(Lesson).id
            initial['object_id'] = lesson_id
        elif module_id:
            initial['content_type'] = ContentType.objects.get_for_model(Module).id
            initial['object_id'] = module_id
        return initial

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'number', 'html_content', 'upload_sound_button')
    search_fields = ('lesson__title', 'number')
    ordering = ['lesson', 'number']
    inlines = [LessonSpeechInline]

    def upload_sound_button(self, obj):
        if obj.module_speeches.exists():
            return obj.module_speeches.first().code
        url = reverse('admin:lessons_lessonspeech_add') + f'?module={obj.id}'
        return format_html('<a class="button" href="{}">+ Pagina</a>', url)

    upload_sound_button.short_description = 'Pagina'
    upload_sound_button.allow_tags = True

class LessonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description', 'upload_sound_button')
    inlines = [ModuleInline]

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