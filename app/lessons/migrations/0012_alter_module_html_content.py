# Generated by Django 3.2.16 on 2025-02-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0011_alter_lessonspeech_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module',
            name='html_content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
