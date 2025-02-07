from django.db import models

class Tag(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    hint_russian = models.CharField(max_length=100)
    hint_finnish = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.code} - {self.name}'

    class Meta:
        verbose_name = 'Znaku'
        verbose_name_plural = 'Znakut'
        ordering = ['id']