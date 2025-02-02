from django import forms
from ..models import LessonSpeech

class LessonSpeechForm(forms.ModelForm):
    class Meta:
        model = LessonSpeech
        fields = '__all__'
