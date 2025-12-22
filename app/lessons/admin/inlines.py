from django.urls import reverse
from django.utils.html import format_html
from nested_admin import (
    NestedGenericTabularInline,
    NestedStackedInline,
    NestedTabularInline,
)

from ..models import Exercise, GrammarComment, LessonSpeech, Module
from .forms import ExerciseForm, ModuleForm


class GrammarCommentInline(NestedTabularInline):
    model = GrammarComment
    extra = 0
    max_num = 1  # Теперь только один комментарий
    fields = ("html_content",)
    classes = ("collapse",)
    verbose_name = "Грамматический комментарий"
    verbose_name_plural = "Грамматический комментарий"

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        from ckeditor.widgets import CKEditorWidget

        formset.form.base_fields["html_content"].widget = CKEditorWidget()
        return formset


class LessonSpeechNestedInline(NestedGenericTabularInline):
    model = LessonSpeech
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 0
    max_num = 1
    fields = ("code", "mp3", "text")


class ExerciseInline(NestedStackedInline):
    model = Exercise
    form = ExerciseForm
    # classes = ('collapse',)
    extra = 0
    fields = ("exercise_type", "data", "has_answers_check")


class ModuleInline(NestedStackedInline):
    model = Module
    form = ModuleForm
    extra = 0
    fields = ("site_url_link", "number", "html_content", "tags", "edit_link")
    inlines = [GrammarCommentInline, LessonSpeechNestedInline]

    readonly_fields = ("site_url_link", "edit_link")

    def site_url_link(self, obj):
        if obj.id:
            return format_html('<a href="/lessons/{}">VIEW PAGE</a>', obj.site_url)
        return ""

    def edit_link(self, obj):
        if obj.id:
            url = reverse("admin:lessons_module_change", args=[obj.id])
            return format_html('<a href="{}">Edit</a>', url)
        return ""

    edit_link.short_description = "Edit Link"
    edit_link.allow_tags = True
    site_url_link.short_description = ""
    site_url_link.allow_tags = True
