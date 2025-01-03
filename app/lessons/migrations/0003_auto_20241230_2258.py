# Generated by Django 3.2.16 on 2024-12-30 22:58

from django.db import migrations, models
import django.db.models.deletion
import lessons.models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0002_remove_lesson_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ['num'], 'verbose_name': 'Uroka', 'verbose_name_plural': 'Urokat'},
        ),
        migrations.CreateModel(
            name='LessonSpeech',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(db_index=True, null=True)),
                ('mp3', models.FileField(blank=True, null=True, upload_to=lessons.models.LessonSpeech.sound_upload_path)),
                ('lesson', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_speech', to='lessons.lesson')),
            ],
            options={
                'verbose_name': 'Pagina',
                'verbose_name_plural': 'Paginat',
            },
        ),
    ]
