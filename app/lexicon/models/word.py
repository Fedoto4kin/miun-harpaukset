from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from krl.settings import LANGUAGE

from lexicon.ortho import strip_soft_signs

from .pos import Pos
from .speech import Speech

KRL_ABC = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ"


class Word(models.Model):

    roman_numeral_validator = RegexValidator(
        regex=r"^[IVXLCDM]+$",
        message="Variant must contain only Roman numerals (I, V, X, L, C, D, M)",
    )

    word = models.CharField(_("Šana"), max_length=128)
    variant = models.CharField(
        _("Variant"),
        max_length=10,
        blank=True,
        null=True,
        default=None,
        validators=[roman_numeral_validator],
        help_text=_("Roman numeral variant (e.g., I, II, III, IV)"),
    )

    word_clean = models.CharField(_("Cleaned Šana"), max_length=128, blank=True)
    pos = models.ForeignKey(Pos, unique=False, on_delete=models.CASCADE)
    speech = models.ForeignKey(Speech, null=True, blank=True, on_delete=models.SET_NULL)
    orig = models.TextField(blank=True)
    alias = models.ManyToManyField("self", blank=True)
    # eg "nedeli" for "Srašnoi"
    additional = models.CharField(
        _("Additional spec"),
        max_length=255,
        blank=True,
        null=True,
        default=None,
        help_text=_(
            "Additional specification or context (e.g., 'nedeli' for 'Srašnoi')"
        ),
    )

    def krl_slugify(self):
        return "".join(
            [i for i in self.word.lower().replace("ü", "y") if i in KRL_ABC.lower()]
        )

    def __str__(self):
        parts = [self.word_clean]
        if self.variant:
            parts.append(f"({self.variant})")
        if self.additional:
            parts.append(f" {self.additional}")

        return " ".join(parts)

    # todo: move to service
    @staticmethod
    def search_prepare(string):
        # todo: filter by KRL_ABC
        # Мягкий знак (ʼ / ’ / ') снимаем — поиск не зависит от канона хранения.
        return strip_soft_signs(string.lower().replace("ü", "y"))

    def save(self, *args, **kwargs):
        self.word_clean = strip_soft_signs(self.word.replace("|", ""))
        super(Word, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Šana"
        verbose_name_plural = "Šanat"


class Definition(models.Model):

    word = models.ForeignKey(
        Word, unique=False, on_delete=models.CASCADE, related_name="definition_set"
    )
    lang = models.CharField(max_length=32, choices=LANGUAGE)
    definition = models.TextField(blank=True)
    definition_lcase = models.TextField(blank=True)

    class Meta:
        ordering = ["-lang"]

    def save(self, *args, **kwargs):
        self.definition_lcase = self.definition.lower()
        super(Definition, self).save(*args, **kwargs)
