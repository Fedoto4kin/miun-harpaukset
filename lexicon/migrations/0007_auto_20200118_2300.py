# Generated by Django 3.0.2 on 2020-01-18 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0006_auto_20200115_0301'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pos',
            options={'verbose_name': 'Šanaloukka'},
        ),
        migrations.AlterModelOptions(
            name='word',
            options={'verbose_name': 'Šana', 'verbose_name_plural': 'Šanat'},
        ),
        migrations.AddField(
            model_name='base',
            name='base_slug',
            field=models.CharField(blank=True, db_index=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='base',
            name='num',
            field=models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]),
        ),
        migrations.AlterField(
            model_name='base',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_set', to='lexicon.Word'),
        ),
        migrations.AlterField(
            model_name='definition',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='definition_set', to='lexicon.Word'),
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=128, verbose_name='Šana'),
        ),
    ]
