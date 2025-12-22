from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from krl.settings import LANGUAGE


class GrammarComment(models.Model):

    module = models.OneToOneField(
        "Module",
        on_delete=models.CASCADE,
        related_name="grammar_comment",  # Изменили на единственное число
        verbose_name="Модуль",
        unique=True,  # Добавляем unique для OneToOne
    )
    html_content = RichTextField("HTML content", blank=True, null=True, default=None)
    lang = models.CharField(max_length=32, choices=LANGUAGE, default="ru")
    summary = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return f"Грамматика: {self.module}"

    class Meta:
        verbose_name = "Грамматический комментарий"
        verbose_name_plural = "Грамматические комментарии"
        indexes = [
            models.Index(fields=["module"]),
        ]
