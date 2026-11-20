"""Backfill definition_lcase: ё → е (reverse search)."""

from django.db import migrations
from django.db.models import F, Q, Value
from django.db.models.functions import Lower, Replace


def forwards(apps, schema_editor):
    Definition = apps.get_model("lexicon", "Definition")
    Definition.objects.filter(
        Q(definition__contains="ё")
        | Q(definition__contains="Ё")
        | Q(definition_lcase__contains="ё")
        | Q(definition_lcase__contains="Ё")
    ).update(
        definition_lcase=Replace(
            Lower(F("definition")),
            Value("ё"),
            Value("е"),
        )
    )


def backwards(apps, schema_editor):
    # Необратимо: исходный ё в lcase не восстанавливаем.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("lexicon", "0034_alter_grammarform_category_komparativa"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
