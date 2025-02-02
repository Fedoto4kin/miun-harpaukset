from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib import admin
from ..models import LessonSpeech, Module

class LessonSpeechInline(GenericTabularInline):
    model = LessonSpeech
    extra = 1
    extra_num = 0
    max_num = 1
    fields = ('code', 'mp3', 'text')

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1
    fields = ('number', 'html_content', 'tags')
