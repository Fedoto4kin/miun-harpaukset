from django.db import models
from uuid import uuid4
from django.utils.text import Truncator


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

    @property
    def media(self):
        if self.mp3:
            self.mp3.name = 'media/' + self.mp3.name
            return self.mp3
        
    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginat'