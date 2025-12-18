from django.db import models


class Pos(models.Model):

    abbr = models.CharField(max_length=32)
    name_ru = models.CharField(max_length=32, default="?")
    name_fi = models.CharField(max_length=32, default="?")

    def __str__(self):
        return self.abbr

    class Meta:
        verbose_name = "Šanaloukka"
