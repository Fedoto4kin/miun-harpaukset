from django.contrib import admin

# Register your models here.
from .models import Word, Pos, Definition, Base

class BaseInline(admin.TabularInline):
    extra = 0
    model = Base
    readonly_fields = ["base_slug"]

class DefinitionInline(admin.TabularInline):
    extra = 0
    model = Definition

class WordAdm(admin.ModelAdmin):
    list_display = ('word','_pos', '_def')
    list_filter = (
        ('pos', admin.RelatedOnlyFieldListFilter),
    )
    search_fields = ('word', 'base_set__base', 'definition_set__definition')
    inlines = [
        DefinitionInline,
        BaseInline,
    ]

    def _pos(self, obj):
    	return ("%s" % obj.pos.abbr)

    def _def(self, obj):
        return ' — '.join([i['definition'] for i in obj.definition_set.values()])


admin.site.site_title = "Ylläpitäjän paikka"
admin.site.site_header = "Ylläpitäjän paikka" 
admin.site.register(Word, WordAdm)