# Generated by Django 3.0.2 on 2020-02-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0010_auto_20200208_1320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='definition',
            options={'ordering': ['-lang']},
        ),
        migrations.AddField(
            model_name='word',
            name='alias',
            field=models.ManyToManyField(blank=True, null=True, related_name='_word_alias_+', to='lexicon.Word'),
        ),
    ]
