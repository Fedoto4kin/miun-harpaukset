from django.db import models
from ckeditor.fields import RichTextField


class GrammarComment(models.Model):
    module = models.ForeignKey(
        "Module",
        on_delete=models.CASCADE,
        related_name="grammar_comments",
        verbose_name="Модуль"
    )
    
    html_content = RichTextField(
        "HTML content",
        blank=True,
        null=True,
        default=None
    )
    
    def __str__(self):
        return f"Грамматика: {self.module} - {f'Комментарий #{self.id}'}"
    
    class Meta:
        verbose_name = "Грамматический комментарий"
        verbose_name_plural = "Грамматические комментарии"
        indexes = [
            models.Index(fields=["module"]),
        ]