from django.db import models
from django.utils.translation import gettext_lazy as _

from .pos import Pos
from .speech import Speech

KRL_ABC = "ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ"


class Word(models.Model):

    word = models.CharField(_("Šana"), max_length=128)
    word_clean = models.CharField(_("Cleaned Šana"), max_length=128, blank=True)
    pos = models.ForeignKey(Pos, unique=False, on_delete=models.CASCADE)
    speech = models.ForeignKey(Speech, null=True, blank=True, on_delete=models.SET_NULL)
    orig = models.TextField(blank=True)
    alias = models.ManyToManyField("self", blank=True)

    def krl_slugify(self):
        return "".join(
            [i for i in self.word.lower().replace("ü", "y") if i in KRL_ABC.lower()]
        )

    def __str__(self):
        return self.word_clean

    # todo: move to service
    @staticmethod
    def search_prepare(string):
        # todo: filter by KRL_ABC
        return string.lower().replace("ü", "y").replace("’", "").replace("'", "")

    def save(self, *args, **kwargs):
        self.word_clean = self.word.replace("|", "").replace("’", "").replace("'", "")
        super(Word, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Šana"
        verbose_name_plural = "Šanat"


class Definition(models.Model):
    LANGUAGE = (
        ("ru", _("Hormiksi")),
        ("fi", _("Šuomekši")),
    )

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
