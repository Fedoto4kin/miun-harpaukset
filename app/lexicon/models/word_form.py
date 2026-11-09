from django.db import models

from .grammar_form import GrammarForm
from .word import Word


class WordFormQuerySet(models.QuerySet):
    def for_search(self, prepared: str, *, prefix: bool = True):
        """
        Поиск по словоформам.

        prefix=True  — istartswith (подсказки).
        prefix=False — точное совпадение form_clean (выдача поиска):
        иначе «elä» тянет eliä через elän.

        Аналитика (пробел в form_clean) исключается, пока в запросе
        нет пробела — иначе «ei» / «olen» заливают выдачу чужими глаголами.
        """
        if prefix:
            qs = self.filter(form_clean__istartswith=prepared)
        else:
            qs = self.filter(form_clean=prepared)
        if " " not in prepared:
            qs = qs.exclude(form_clean__contains=" ")
        return qs


class WordForm(models.Model):
    """Сгенерированная словоформа леммы."""

    word = models.ForeignKey(
        Word, on_delete=models.CASCADE, related_name="wordform_set"
    )
    grammar_form = models.ForeignKey(
        GrammarForm, on_delete=models.CASCADE, related_name="wordform_set"
    )
    form = models.CharField(max_length=256)
    form_clean = models.CharField(max_length=256, blank=True, db_index=True)

    objects = WordFormQuerySet.as_manager()

    class Meta:
        verbose_name = "Šanan muodo"
        verbose_name_plural = "Šanan muodoloi"
        # Несколько орфографий на один слот (альтернативные основы мн.ч.)
        unique_together = [("word", "grammar_form", "form")]
        ordering = ["grammar_form__sort_order", "id"]
        indexes = [
            models.Index(fields=["form_clean"]),
            models.Index(fields=["word", "grammar_form"]),
        ]

    def __str__(self):
        return f"{self.form} [{self.grammar_form.code}]"

    def save(self, *args, **kwargs):
        self.form_clean = Word.search_prepare(self.form)
        super().save(*args, **kwargs)
