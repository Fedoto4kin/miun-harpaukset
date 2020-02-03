from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator


class Pos(models.Model):
    
    abbr = models.CharField(max_length=32)
    name_ru = models.CharField(max_length=32, default='?')
    name_fi = models.CharField(max_length=32, default='?')

    def __str__(self):
           return self.abbr

    class Meta:
        verbose_name = 'Šanaloukka'

class Word(models.Model):
    
    KRL_ABC = 'ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ'

    #TODO: Correct sorting by karelian abc
    word = models.CharField(_('Šana'), max_length=128)
    pos = models.ForeignKey(Pos, unique=False, on_delete=models.CASCADE)
    orig = models.TextField(blank=True)

    def __str__(self):
        return self.word

    class Meta:
        verbose_name = 'Šana'
        verbose_name_plural = 'Šanat'


class Definition(models.Model):

    LANGUAGE = (
        ('ru', _('Hormiksi')),
        ('fi', _('Šuomekši')),
    )
    
    word = models.ForeignKey(Word, unique=False, on_delete=models.CASCADE,  related_name='definition_set')
    lang =  models.CharField(max_length=32, choices=LANGUAGE)
    definition = models.TextField(blank=True)
    
    class Meta:
        unique_together = ("word", "lang")
    

class Base(models.Model):
    
    word = models.ForeignKey(Word, unique=False, on_delete=models.CASCADE, related_name='base_set')
    num = models.IntegerField(choices=((int(x), x) for x in range(0,8)))
    base = models.CharField(max_length=128)
    base_slug = models.CharField(max_length=128, db_index=True, blank=True)
    
    class Meta:
        unique_together = ("num", "base", "word")

    def krl_slugify(self, string):
        return ''.join([i for i in string if i.isalpha()]).lower().replace('ü','y')

    def save(self, *args, **kwargs):
        self.base_slug = self.krl_slugify(self.base)
        super(Base, self).save(*args, **kwargs)