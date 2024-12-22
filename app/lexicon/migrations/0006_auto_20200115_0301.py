# Generated by Django 3.0.2 on 2020-01-15 03:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0005_auto_20200115_0110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='base',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base', to='lexicon.Word'),
        ),
        migrations.AlterField(
            model_name='definition',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definition', to='lexicon.Word'),
        ),
        migrations.AlterUniqueTogether(
            name='base',
            unique_together={('num', 'base', 'word')},
        ),
    ]
