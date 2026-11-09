from django import forms
from django.contrib import admin

from .models import Definition, GrammarForm, Speech, Stem, Word, WordForm
from .models.word_form import _normalize_alt_list


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


class WordFormInlineForm(forms.ModelForm):
    alt_spellings_text = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 2, "cols": 30}),
        label="Alt spellings",
        help_text="По одному на строку (или через запятую). Только поиск, не парадигма.",
    )

    class Meta:
        model = WordForm
        fields = ("grammar_form", "form", "form_clean")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        alts = []
        if self.instance and self.instance.pk:
            alts = self.instance.alt_spellings or []
        self.fields["alt_spellings_text"].initial = "\n".join(alts)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.alt_spellings = _normalize_alt_list(
            self.cleaned_data.get("alt_spellings_text")
        )
        if commit:
            instance.save()
        return instance


class WordFormInline(admin.TabularInline):
    """Канон readonly; альты написания — редактируемые."""

    model = WordForm
    form = WordFormInlineForm
    extra = 0
    max_num = 0
    can_delete = False
    show_change_link = False
    ordering = ("grammar_form__sort_order",)
    fields = ("grammar_form", "form", "form_clean", "alt_spellings_text")
    readonly_fields = ("grammar_form", "form", "form_clean")

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
