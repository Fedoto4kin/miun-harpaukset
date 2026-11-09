from django.db import models
from django.db.models import BooleanField, Q
from django.db.models.expressions import RawSQL

from .grammar_form import GrammarForm
from .word import Word


def _normalize_alt_list(raw) -> list[str]:
    """Список строк из JSON / textarea (по строке или через запятую)."""
    if not raw:
        return []
    if isinstance(raw, str):
        parts = []
        for line in raw.replace(",", "\n").splitlines():
            s = line.strip()
            if s:
                parts.append(s)
        return parts
    if isinstance(raw, (list, tuple)):
        return [str(x).strip() for x in raw if str(x).strip()]
    return []


class WordFormQuerySet(models.QuerySet):
    def for_search(self, prepared: str, *, prefix: bool = True):
        """
        Поиск по словоформам и alt_spellings_clean.

        prefix=True  — istartswith (подсказки).
        prefix=False — точное совпадение (выдача поиска).

        Аналитика (пробел в form_clean) исключается, пока в запросе нет пробела.
        """
        if not prepared:
            return self.none()

        if prefix:
            form_q = Q(form_clean__istartswith=prepared)
            alt_op = "LIKE"
            alt_arg = prepared + "%"
        else:
            form_q = Q(form_clean=prepared)
            alt_op = "="
            alt_arg = prepared

        alt_sql = RawSQL(
            "EXISTS ("
            "  SELECT 1 FROM jsonb_array_elements_text("
            "    COALESCE(alt_spellings_clean, '[]'::jsonb)"
            "  ) AS alt WHERE alt " + alt_op + " %s"
            ")",
            [alt_arg],
            output_field=BooleanField(),
        )
        qs = self.annotate(_alt_hit=alt_sql).filter(form_q | Q(_alt_hit=True))
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
    # Разговорные / песенные написания — только поиск, не парадигма.
    alt_spellings = models.JSONField(default=list, blank=True)
    alt_spellings_clean = models.JSONField(default=list, blank=True)

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

    def search_surfaces(self):
        """Пары (surface, clean): канон + альты."""
        pairs = [(self.form, self.form_clean)]
        alts = self.alt_spellings or []
        cleans = self.alt_spellings_clean or []
        # Если clean ещё не сохранён — посчитаем на лету.
        if len(cleans) != len(alts):
            cleans = [Word.search_prepare(a) for a in alts]
        for alt, clean in zip(alts, cleans):
            pairs.append((alt, clean))
        return pairs

    def surface_matching(self, prepared: str, *, prefix: bool = False) -> str:
        """Какую орфографию показать в цепочке поиска."""
        for surface, clean in self.search_surfaces():
            if prefix:
                if clean.startswith(prepared):
                    return surface
            elif clean == prepared:
                return surface
        return self.form

    def save(self, *args, **kwargs):
        self.form_clean = Word.search_prepare(self.form)
        alts = _normalize_alt_list(self.alt_spellings)
        self.alt_spellings = alts
        self.alt_spellings_clean = [Word.search_prepare(a) for a in alts]
        super().save(*args, **kwargs)
