from django.db import models

class Lesson(models.Model):

    num = models.IntegerField()
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.num}. {self.title}'

    @property    
    def full_name(self):
        return self.__str__

    class Meta:
        verbose_name = 'Uroka'
        verbose_name_plural = 'Urokat'
        ordering = ['num']
