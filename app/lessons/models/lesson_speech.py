import os
import re
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from .lesson import Lesson  # Import the Lesson model

class LessonSpeech(models.Model):

    def sound_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]  
        unique_filename = f"{uuid.uuid4()}{ext}"
        
        if self.code:
            directory = self.code.split('.')[0]
        else:
            directory = '0'
        
        return os.path.join('lessons', directory, unique_filename)
    
    text = models.TextField(blank=False, null=True, db_index=True)
    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )
    lesson = models.OneToOneField(
        Lesson,  # Use the imported Lesson model
        on_delete=models.CASCADE, 
        related_name='lesson_speech',
        null=True,
        blank=True
    )
    code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        help_text="X.Y (1.0, 1.1, 2.1)"
    )

    @property
    def media(self):
        return self.mp3

    def __str__(self):
        return self.text

    def clean(self):
        super().clean()
        if self.code and not re.match(r'^\d+\.\d+$', self.code):
            raise ValidationError({'code': 'Код должен быть в формате X.Y (например, 1.0, 1.1, 2.1 и т.д.)'})

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginat'