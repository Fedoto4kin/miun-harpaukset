# Generated by Django 3.2.16 on 2025-02-08 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0019_alter_exercise_exercise_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='exercise_type',
            field=models.CharField(choices=[('FillBlank', 'Fill in the Blank Words'), ('SyllableAssembly', 'Syllable Assembly'), ('FillBlankText', 'Fill in the Blank Text'), ('SentenceAssembly', 'Sentence Assembly'), ('MatchPair', 'Match the Pair')], max_length=50),
        ),
    ]
