from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Lesson, LessonSpeech, Module

class LessonSpeechInline(admin.TabularInline):
    model = LessonSpeech
    extra = 1  
    fields = ('code', 'mp3', 'text')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1  
    fields = ('number', 'html_content', 'tags')


class LessonSpeechAdmin(admin.ModelAdmin):
    list_display = ('code', 'mp3')
    search_fields = ('code',)
    ordering = ['-code']

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        lesson_id = request.GET.get('lesson')
        if lesson_id:
            initial['lesson'] = lesson_id
        return initial

class ModuleAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'number', 'html_content')
    search_fields = ('lesson__title', 'number') 
    ordering = ['lesson', 'number']


class LessonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'description','upload_sound_button')
    inlines = [LessonSpeechInline, ModuleInline]

    def upload_sound_button(self, obj):
        if obj.has_lesson_speech():
            return obj.speech.code
        url = reverse('admin:lessons_lessonspeech_add') + f'?lesson={obj.id}'
        return format_html('<a class="button" href="{}">+ Pagina</a>', url)
        
    upload_sound_button.short_description = 'Pagina'
    upload_sound_button.allow_tags = True


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonSpeech, LessonSpeechAdmin)
admin.site.register(Module, ModuleAdmin)