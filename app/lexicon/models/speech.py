from django.db import models
from django.utils.text import Truncator
from uuid import uuid4


class Speech(models.Model):
    
    def sound_upload_path(self, filename):
        filename = "%s.%s" % (uuid4(), filename.split('.')[-1])
        dir_id = ord(self.text[0]) % 10
        return 'lexicon/speech_{0}/{1}'.format(dir_id, filename)
    
    text = models.TextField(blank=False, null=True, db_index=True)
    mp3 = models.FileField(
        upload_to=sound_upload_path,
        null=True,
        blank=True,
        editable=True,
    )

    @property
    def media(self):
        return self.mp3

    def __str__(self):
        return Truncator(self.text).words(1)

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginat'