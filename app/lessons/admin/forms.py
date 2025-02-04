import json
from django import forms
from ckeditor.widgets import CKEditorWidget
from django_json_widget.widgets import JSONEditorWidget
from ..models import LessonSpeech, Module, Exercise
from .widgets import HideListenTagWidget

class LessonSpeechForm(forms.ModelForm):
    class Meta:
        model = LessonSpeech
        fields = '__all__'


class ModuleForm(forms.ModelForm):
    html_content = forms.CharField(widget=CKEditorWidget()) 

    class Meta:
        model = Module
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget = HideListenTagWidget()


class ExerciseForm(forms.ModelForm):
    
    class Meta:
        model = Exercise
        fields = '__all__'
        widgets = {
            'data': JSONEditorWidget(attrs={'class': 'json-editor'}),
        }
