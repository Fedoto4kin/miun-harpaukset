# Generated by Django 3.0.2 on 2020-01-14 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=128, unique=True, verbose_name='Word')),
                ('pos', models.CharField(max_length=10, verbose_name='Part of speech')),
            ],
        ),
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang', models.CharField(choices=[('ru', 'Hormiksi'), ('fi', 'Šuomekši')], max_length=32)),
                ('definition', models.TextField()),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lexicon.Word')),
            ],
            options={
                'unique_together': {('word', 'lang')},
            },
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(choices=[('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7)])),
                ('base', models.CharField(max_length=128)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lexicon.Word')),
            ],
            options={
                'unique_together': {('num', 'base')},
            },
        ),
    ]
