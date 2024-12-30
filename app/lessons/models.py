from django.db import models

class Lesson(models.Model):

    num = models.IntegerField()
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Uroka'
        verbose_name_plural = 'Urokat'
