from django.db import models


class GrammarForm(models.Model):
    """Справочник слотов парадигмы (ярлыки krl/ru)."""

    class Category(models.TextChoices):
        NOUN = "noun", "Nimišana"
        VERB = "verb", "Aziešana"
        PRON = "pron", "Nimenšijalline"
        # Продуктивные уменьшительные на базе s. (поиск; не в таблице парадигмы)
        DIMINUTIVE = "diminutive", "Pieniskö"
        # Притяжательные -ni / -š (поиск; не в таблице парадигмы)
        POSSESSIVE = "possessive", "Omistuš"
        # Сравнительная степень a. на -mbi (поиск; не в таблице парадигмы)
        COMPARATIVE = "comparative", "Komparativa"

    code = models.CharField(max_length=32, unique=True)
    name_krl = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)
    category = models.CharField(
        max_length=16, choices=Category.choices, default=Category.NOUN
    )
    sort_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Muutoš"
        verbose_name_plural = "Muutokšet"
        ordering = ["sort_order", "code"]

    def __str__(self):
        return f"{self.name_krl} ({self.code})"
