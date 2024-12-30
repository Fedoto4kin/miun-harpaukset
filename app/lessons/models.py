from django.db import models
import os
import re
import uuid


class LessonSpeech(models.Model):

    def sound_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]  
        unique_filename = f"{uuid.uuid4()}{ext}"

        return os.path.join('lessons', '0', unique_filename)
    
    text = models.TextField(blank=False, null=True, db_index=True)
    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )
    lesson = models.OneToOneField(
        'Lesson', 
        on_delete=models.CASCADE, 
        related_name='lesson_speech',
        null=True,
        blank=True
    )

    @property
    def media(self):
        return self.mp3

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginat'


class Lesson(models.Model):
    num = models.IntegerField()
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.num}. {self.title}'
    
    @property
    def speech(self):
        return self.lesson_speech

    @property
    def full_name(self):
        return self.__str__

    class Meta:
        verbose_name = 'Uroka'
        verbose_name_plural = 'Urokat'
        ordering = ['num']