from django.db import models
from .lesson import Lesson  # Import the Lesson model
from .tag import Tag  # Import the Tag model

class Module(models.Model):
    lesson = models.ForeignKey(
        Lesson,  # Use the imported Lesson model
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Urokka'
    )
    number = models.IntegerField()
    html_content = models.TextField()
    tags = models.ManyToManyField(
        Tag,  # Use the imported Tag model
        related_name='modules',
        blank=True,
        verbose_name='Znakut'
    )

    def __str__(self):
        return f'{self.lesson.num}.{self.number} - {self.lesson.title}'

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        unique_together = ('lesson', 'number')
        ordering = ['lesson', 'number']