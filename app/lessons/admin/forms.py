from django import forms
from django_json_widget.widgets import JSONEditorWidget

from krl.ckeditor5_widget import KrlCKEditor5Widget

from ..models import Exercise, LessonSpeech, Module
from .widgets import HideListenTagWidget, LinkToFrontendWidget


class LessonSpeechForm(forms.ModelForm):
    class Meta:
        model = LessonSpeech
        fields = "__all__"


class ModuleForm(forms.ModelForm):
    module_url = forms.CharField(widget=forms.HiddenInput(), required=False)
    site_url_display = forms.CharField(widget=LinkToFrontendWidget(), required=False)

    class Meta:
        model = Module
        fields = "__all__"
        widgets = {
            "html_content": KrlCKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="default"
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["tags"].widget = HideListenTagWidget()
        self.fields["html_content"].required = False

        if self.instance.pk:
            self.fields["module_url"].initial = f"/lessons/{self.instance.site_url}"
            self.fields["site_url_display"].initial = self.fields["module_url"].initial


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = "__all__"
        widgets = {"data": JSONEditorWidget(attrs={"class": "json-editor"})}
