import re
from django.db import models
from django.utils.translation import gettext as _
from slugify import slugify
from uuid import uuid4
from django.utils.text import Truncator

KRL_ABC = 'ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ'


class Speech(models.Model):

    def sound_upload_path(self, filename):
        filename = "%s.%s" % (uuid4(), filename.split('.')[-1])
        dir_id = ord(self.text[0]) % 10
        return 'lexicon/speech_{0}/{1}'.format(dir_id, filename)

    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )
    text = models.TextField(blank=False, null=True, db_index=True)

    def __str__(self):
        return Truncator(self.text).words(1)


class Pos(models.Model):

    abbr = models.CharField(max_length=32)
    name_ru = models.CharField(max_length=32, default='?')
    name_fi = models.CharField(max_length=32, default='?')

    def __str__(self):
        return self.abbr

    class Meta:
        verbose_name = 'Šanaloukka'


class Word(models.Model):

    word = models.CharField(_('Šana'), max_length=128)
    pos = models.ForeignKey(Pos, unique=False, on_delete=models.CASCADE)
    speech = models.ForeignKey(Speech, null=True, blank=True, on_delete=models.SET_NULL)
    orig = models.TextField(blank=True)
    alias = models.ManyToManyField('self', blank=True)

    @staticmethod
    def get_krl_abc():
        return KRL_ABC

    def __str__(self):
        return self.base_set.get(num=0).base

    @staticmethod
    def search_prepare(string):
        return string.lower().replace('ü', 'y').replace('’', '').replace('\'', '') #TODO: bulk filter 'bads' non-aphabeth and whitespace


    class Meta:
        verbose_name = 'Šana'
        verbose_name_plural = 'Šanat'


class Definition(models.Model):
    LANGUAGE = (
        ('ru', _('Hormiksi')),
        ('fi', _('Šuomekši')),
    )

    word = models.ForeignKey(Word, unique=False, on_delete=models.CASCADE, related_name='definition_set')
    lang = models.CharField(max_length=32, choices=LANGUAGE)
    definition = models.TextField(blank=True)
    definition_lcase = models.TextField(blank=True)

    class Meta:
        ordering = ['-lang']

    def save(self, *args, **kwargs):
        self.definition_lcase = self.definition.lower()
        super(Definition, self).save(*args, **kwargs)


class Base(models.Model):

    BASES = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
    )

    word = models.ForeignKey(Word, unique=False, on_delete=models.CASCADE, related_name='base_set')
    num = models.IntegerField(choices=BASES)
    base = models.CharField(max_length=128)
    base_slug = models.CharField(max_length=128, db_index=True, blank=True)
    base_slug_diacritic = models.CharField(max_length=128, db_index=True, blank=True)

    @staticmethod
    def get_krl_abc():
        return KRL_ABC

    def __str__(self):
        return self.base

    class Meta:
        unique_together = ("num", "base", "word")

    def krl_slugify(self, string):
        return ''.join([i for i in string.lower().replace('ü', 'y') if i in self.get_krl_abc().lower()])

    def save(self, *args, **kwargs):
        self.base_slug = slugify(self.base)
        self.base_slug_diacritic = self.krl_slugify(self.base)
        super(Base, self).save(*args, **kwargs)


class GrammarForm(models.Model):
    name = models.CharField(max_length=128, db_index=True, blank=True)
    pos = models.ManyToManyField(Pos)
    pre = models.CharField(max_length=128, blank=True, default='')
    end = models.CharField(max_length=128, blank=True, default='')
    base = models.IntegerField(choices=Base.BASES)
    # lambda function (?)
    rule = models.CharField(max_length=1024, blank=True, default='')
    hidden = models.BooleanField(default=False)


class WordForm(models.Model):

    @staticmethod
    def vowel_garmonize(suff):
        """
        Returns harmonized suffix by vovel of base
        if base contains a, o or u -> a suff
        else ä, ö and y in suff
        """
        # TODO
        return suff

    word = models.ForeignKey(Word, unique=False, on_delete=models.CASCADE, related_name='form_set')
    form = models.ForeignKey(GrammarForm, unique=False, on_delete=models.CASCADE, related_name='form')
    form_slug = models.CharField(max_length=128, db_index=True, blank=True)
    form_slug_diacritic = models.CharField(max_length=128, db_index=True, blank=True)
