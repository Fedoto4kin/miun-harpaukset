from django.db import models
from ckeditor.fields import RichTextField


class GrammarTable(models.Model):
    """
    Модель для хранения грамматических таблиц
    Простая структура: заголовок + HTML-контент с CKEditor
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Заголовок таблицы",
        help_text="Название грамматической таблицы"
    )
    
    html_content = RichTextField(
        verbose_name="HTML содержимое",
        help_text="HTML-код таблицы для отображения. Используйте редактор для форматирования.",
        config_name='default'
    )
    
    order = models.IntegerField(
        default=0,
    )
    
    is_published = models.BooleanField(
        default=True,
    )

    class Meta:
        verbose_name = "Tabliča"
        verbose_name_plural = "Tabličat"
        ordering = ['-order']
        indexes = [
            models.Index(fields=['order', 'is_published']),
        ]

    def __str__(self):
        return self.title
