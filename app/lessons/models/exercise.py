from django.db import models
from django.core.serializers.json import DjangoJSONEncoder
from enum import Enum

class ExerciseType(Enum):
    FILL_BLANK = "FillBlank"
    #todo: Add more types

class Exercise(models.Model):
    module = models.ForeignKey(
        'Module',
        on_delete=models.CASCADE,
        related_name='exercises'
    )
    exercise_type = models.CharField(
        max_length=50,
        choices=[(tag.value, tag.name) for tag in ExerciseType],
    )
    data = models.JSONField(
        encoder=DjangoJSONEncoder,
        default=dict,
        blank=True
    )

    class Meta:
        verbose_name = 'Annanda'
        verbose_name_plural = 'Annandat'

    def __str__(self):
        return f"{self.get_exercise_type_display()}: {self.module}"