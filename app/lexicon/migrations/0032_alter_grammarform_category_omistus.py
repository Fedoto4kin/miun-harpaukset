# Generated manually for Omistus → Omistuš label

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lexicon", "0031_grammarform_category_choices"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grammarform",
            name="category",
            field=models.CharField(
                choices=[
                    ("noun", "Nimišana"),
                    ("verb", "Aziešana"),
                    ("pron", "Nimenšijalline"),
                    ("diminutive", "Pieniškö"),
                    ("possessive", "Omistuš"),
                ],
                default="noun",
                max_length=16,
            ),
        ),
    ]
