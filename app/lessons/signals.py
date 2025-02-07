from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LessonSpeech, Module, Tag, Exercise


LISTEN_TAG_CODE = 'listen'
KEY_TAG_CODE = 'key'


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


@receiver(post_save, sender=Exercise)
def add_key_tag(sender, instance, created, **kwargs):
    if created:
        key_tag, created = Tag.objects.get_or_create(
            code=KEY_TAG_CODE,
            defaults={
                'code': KEY_TAG_CODE,
                'name': 'Avuan',
                'hint_russian': 'Ключ',
                'hint_finnish': 'Avain'
            }
        )
        instance.module.tags.add(key_tag)
    else:
        check_and_remove_key_tag(instance.module)


@receiver(post_delete, sender=Exercise)
def remove_key_tag(sender, instance, **kwargs):
    check_and_remove_key_tag(instance.module)


def check_and_remove_key_tag(module):
    if not module.exercises.exists():
        key_tag = Tag.objects.filter(code=KEY_TAG_CODE).first()
        if key_tag:
            module.tags.remove(key_tag)
