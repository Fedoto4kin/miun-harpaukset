# Generated by Django 3.2.16 on 2025-02-09 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0020_alter_exercise_exercise_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='has_ansers_check',
            field=models.BooleanField(default=True),
        ),
    ]
