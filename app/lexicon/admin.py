from django.contrib import admin

# Register your models here.
from .models import *


class BaseInline(admin.TabularInline):
    extra = 0
    model = Base
    readonly_fields = ["base_slug", "base_slug_diacritic"]


class DefinitionInline(admin.TabularInline):
    extra = 0
    exclude = ('definition_lcase',)
    model = Definition


class WordAdm(admin.ModelAdmin):
    list_display = ('word', '_pos', '_def')
    list_filter = (
        ('pos', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('word', 'base_set__base', 'definition_set__definition')
    inlines = [
        DefinitionInline,
        BaseInline,
    ]

    @staticmethod
    def _pos(self):
        return "%s" % self.pos.abbr

    @staticmethod
    def _def(self):
        return ' — '.join([i['definition'] for i in self.definition_set.values()])


class SpeechAdmin(admin.ModelAdmin):
    search_fields = ('text',)


admin.site.site_title = "Ylläpitäjän paikka"
admin.site.site_header = "Ylläpitäjän paikka"
admin.site.register(Word, WordAdm)
admin.site.register(Speech, SpeechAdmin)
