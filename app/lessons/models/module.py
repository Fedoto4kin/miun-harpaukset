from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor.fields import RichTextField
from .lesson import Lesson  # Import the Lesson model
from .tag import Tag  # Import the Tag model
from .lesson_speech import LessonSpeech

class Module(models.Model):
    # Ваши поля модели
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Urokka'
    )
    number = models.IntegerField()
    html_content = RichTextField(
        verbose_name='HTML',
        blank=True,
        null=True,
        default=None
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='modules',
        blank=True,
        verbose_name='Znakut'
    )

    module_speeches = GenericRelation(
        LessonSpeech,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='module'
    )

    @property
    def speech(self):
        return self.module_speeches.first()
    
    @property
    def exercise(self):
        """Return module Exercise if exists"""
        if hasattr(self, 'exercise'):
            return self.exercise
        return None
    
    @property
    def site_url(self):
        return f"{self.lesson.number}/{self.id}"

    def __str__(self):
        return f'{self.lesson.title} - {self.lesson.number}.{self.number}'
    
    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        unique_together = ('lesson', 'number')
        ordering = ['number']

