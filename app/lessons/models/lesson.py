from django.db import models
from django.contrib.contenttypes.fields import GenericRelation 
from .lesson_speech import LessonSpeech

class Lesson(models.Model):
    num = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    lesson_speeches = GenericRelation(
        LessonSpeech,
        content_type_field='content_type',
        object_id_field='object_id',
        related_query_name='lesson'
    )

    def __str__(self):
        return f'{self.num}. {self.title}'
    
    @property
    def speech(self):
        return self.lesson_speeches.first()

    @property
    def full_name(self):
        return self.__str__()
    
    def has_lesson_speech(self):
        return self.lesson_speeches.exists()

    class Meta:
        verbose_name = 'Uroka'
        verbose_name_plural = 'Urokat'
        ordering = ['num']