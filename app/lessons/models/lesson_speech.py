import os
import re
import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class LessonSpeech(models.Model):

    def sound_upload_path(self, filename):
        ext = os.path.splitext(filename)[1]
        unique_filename = f"{uuid.uuid4()}{ext}"

        if self.code:
            directory = self.code.split(".")[0]
        else:
            directory = "0"

        return os.path.join("lessons", directory, unique_filename)

    text = models.TextField(blank=True, null=True, db_index=True)
    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        limit_choices_to=Q(app_label="lessons", model="lesson")
        | Q(app_label="lessons", model="module"),
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        unique=True,
        help_text="X.Y (1.0, 1.1, 2.1)",
    )

    @property
    def media(self):
        return self.mp3

    def __str__(self):
        return self.code

    def clean(self):
        super().clean()
        if self.code and not re.match(r"^\d+\.\d+$", self.code):
            raise ValidationError(
                {
                    "code": "Код должен быть в формате X.Y (например, 1.0, 1.1, 2.1 и т.д.)"
                }
            )

    class Meta:
        verbose_name = "Pagina"
        verbose_name_plural = "Paginat"
