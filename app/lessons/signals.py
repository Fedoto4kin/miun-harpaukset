from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LessonSpeech, Module, Tag


LISTEN_TAG_CODE = 'listen'


@receiver(post_save, sender=LessonSpeech)
def add_tell_tag_on_speech_save(sender, instance, **kwargs):

    if instance.content_object and isinstance(instance.content_object, Module):
        module = instance.content_object
        tell_tag, created = Tag.objects.get_or_create(
            code=LISTEN_TAG_CODE, 
            defaults={
                'code': LISTEN_TAG_CODE, 
                'name': 'Kuundele da tačkuta! / Kuundele oigie varianta!', 
                'hint_russian': 'Послушай и повтори / Послушай правильный вариант', 
                'hint_finnish': 'Kuuntele ja toista / Kuuntele oikea vaihtoehto'
                }
        )
        if instance.mp3:
            module.tags.add(tell_tag)
        else:
            module.tags.remove(tell_tag)


@receiver(post_delete, sender=LessonSpeech)
def remove_tell_tag_on_speech_delete(sender, instance, **kwargs):

    if instance.content_object and isinstance(instance.content_object, Module):
        module = instance.content_object
        tell_tag = Tag.objects.filter(code=LISTEN_TAG_CODE).first()
        if tell_tag:
            module.tags.remove(tell_tag)
