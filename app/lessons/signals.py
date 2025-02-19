from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import LessonSpeech, Module, Tag, Exercise

LISTEN_TAG_CODE = 'listen'
KEY_TAG_CODE = 'key'

@receiver(post_save, sender=LessonSpeech)
@receiver(post_delete, sender=LessonSpeech)
def update_listen_tag_on_speech_change(sender, instance, **kwargs):
    if instance.content_object and isinstance(instance.content_object, Module):
        module = instance.content_object
        check_and_update_listen_tag(module)

@receiver(post_save, sender=Module)
def update_listen_tag_on_module_save(sender, instance, **kwargs):
    check_and_update_listen_tag(instance)

def check_and_update_listen_tag(module):
    tell_tag, _ = Tag.objects.get_or_create(
        code=LISTEN_TAG_CODE,
        defaults={
            'code': LISTEN_TAG_CODE,
            'name': 'Kuundele da tačkuta! / Kuundele oigie varianta!',
            'hint_russian': 'Послушай и повтори / Послушай правильный вариант',
            'hint_finnish': 'Kuuntele ja toista / Kuuntele oikea vaihtoehto'
        }
    )
    if module.lessonspeech_set.exists():
        module.tags.add(tell_tag)
    else:
        module.tags.remove(tell_tag)

@receiver(post_save, sender=Exercise)
def add_key_tag(sender, instance, created, **kwargs):
    key_tag, _ = Tag.objects.get_or_create(
        code=KEY_TAG_CODE,
        defaults={
            'code': KEY_TAG_CODE,
                'name': 'Avuan',
                'hint_russian': 'Ключ',
                'hint_finnish': 'Avain'
            }
    )
    if instance.has_answers_check:
        instance.module.tags.add(key_tag)
    check_and_update_key_tag(instance.module)

@receiver(post_delete, sender=Exercise)
def remove_key_tag(sender, instance, **kwargs):
    check_and_update_key_tag(instance.module)

def check_and_update_key_tag(module):
    key_tag = Tag.objects.filter(code=KEY_TAG_CODE).first()
    if key_tag:
        if module.exercises.filter(has_answers_check=True).exists():
            module.tags.add(key_tag)
        else:
            module.tags.remove(key_tag)
