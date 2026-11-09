from django.contrib import admin

from .models import Definition, GrammarForm, Speech, Stem, Word, WordForm


class DefinitionInline(admin.TabularInline):
    extra = 0
    exclude = ("definition_lcase",)
    model = Definition


class StemInline(admin.TabularInline):
    """Только просмотр основ; правки через import_stems."""

    model = Stem
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = False
    ordering = ("number", "alt")
    fields = ("number", "alt", "form", "stem_type", "special_mark")
    readonly_fields = fields

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class WordFormInline(admin.TabularInline):
    """Только просмотр словоформ; правки через generate_wordforms."""

    model = WordForm
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = False
    ordering = ("grammar_form__sort_order",)
    fields = ("grammar_form", "form", "form_clean")
    readonly_fields = fields
    raw_id_fields = ()

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class WordAdm(admin.ModelAdmin):
    list_display = ("word", "_pos", "_def")
    list_filter = (("pos", admin.RelatedOnlyFieldListFilter),)
    search_fields = ("word", "definition_set__definition")
    inlines = [
        DefinitionInline,
        StemInline,
        WordFormInline,
    ]

    @staticmethod
    def _pos(self):
        return "%s" % self.pos.abbr

    @staticmethod
    def _def(self):
        return " — ".join([i["definition"] for i in self.definition_set.values()])


class SpeechAdmin(admin.ModelAdmin):
    search_fields = ("text",)


class GrammarFormAdmin(admin.ModelAdmin):
    list_display = ("code", "name_krl", "name_ru", "category", "sort_order")
    list_filter = ("category",)
    search_fields = ("code", "name_krl", "name_ru")
    ordering = ("sort_order", "code")


admin.site.site_title = "Izännän paikka"
admin.site.site_header = "Izännän paikka"
admin.site.register(Word, WordAdm)
admin.site.register(Speech, SpeechAdmin)
admin.site.register(GrammarForm, GrammarFormAdmin)
