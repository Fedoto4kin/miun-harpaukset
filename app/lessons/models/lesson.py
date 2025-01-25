from django.db import models

class Lesson(models.Model):
    num = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    description = models.TextField()
    is_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.num}. {self.title}'
    
    @property
    def speech(self):
        return self.lesson_speech

    @property
    def full_name(self):
        return self.__str__
    
    def has_lesson_speech(self):
        if hasattr(self, 'lesson_speech'):
            return self.lesson_speech.code
        return False

    class Meta:
        verbose_name = 'Uroka'
        verbose_name_plural = 'Urokat'
        ordering = ['num']