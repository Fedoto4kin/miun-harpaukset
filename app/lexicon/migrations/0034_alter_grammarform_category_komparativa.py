# Generated manually for comparative (-mbi) search-only category

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lexicon", "0033_alter_grammarform_category_pienisko"),
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
                    ("comparative", "Komparativa"),
                ],
                default="noun",
                max_length=16,
            ),
        ),
    ]
