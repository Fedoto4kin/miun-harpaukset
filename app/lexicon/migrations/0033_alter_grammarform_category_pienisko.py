# Generated manually for Pieniškö → Pieniskö label

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lexicon", "0032_alter_grammarform_category_omistus"),
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
                    ("diminutive", "Pieniskö"),
                    ("possessive", "Omistuš"),
                ],
                default="noun",
                max_length=16,
            ),
        ),
    ]
