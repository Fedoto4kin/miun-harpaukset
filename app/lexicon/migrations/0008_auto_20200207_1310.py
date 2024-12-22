# Generated by Django 3.0.2 on 2020-02-07 13:10

from django.db import migrations, models
import django.db.models.deletion
import lexicon.models


class Migration(migrations.Migration):

    dependencies = [
        ('lexicon', '0007_auto_20200118_2300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Speech',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mp3', models.FileField(blank=True, null=True, upload_to=lexicon.models.Speech.sound_upload_path)),
                ('text', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='pos',
            name='name_fi',
            field=models.CharField(default='?', max_length=32),
        ),
        migrations.AlterField(
            model_name='pos',
            name='name_ru',
            field=models.CharField(default='?', max_length=32),
        ),
        migrations.AddField(
            model_name='word',
            name='speech',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lexicon.Speech'),
        ),
    ]