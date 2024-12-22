from django.db import models


class Lesson(models.model):

    num = models.IntegerField()
    name = models.ChartField(max_length=255)
    title = models.ChartField(max_length=255)
    description = models.TextField()


class Speech(models.Model):

    def sound_upload_path(self, filename):
        filename = "%s.%s" % (uuid4(), filename.split('.')[-1])
        dir_id = ord(self.text[0]) % 10
        return '/speech_{0}/{1}'.format(dir_id, filename)

    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )
    text = models.TextField(blank=False, null=True, db_index=True)

    def __str__(self):
        return Truncator(self.text).words(1)

    @property
    def media(self):
        if self.mp3:
            self.mp3.name = 'media/' + self.mp3.name
            return self.mp3