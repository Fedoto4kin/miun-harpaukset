# Generated by Django 3.2.16 on 2024-12-31 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0003_auto_20241230_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='num',
            field=models.IntegerField(unique=True),
        ),
    ]
