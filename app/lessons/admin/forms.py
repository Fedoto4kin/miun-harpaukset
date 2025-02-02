from django import forms
from ..models import LessonSpeech, Module
from .widgets import HideListenTagWidget

class LessonSpeechForm(forms.ModelForm):
    class Meta:
        model = LessonSpeech
        fields = '__all__'


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget = HideListenTagWidget()
