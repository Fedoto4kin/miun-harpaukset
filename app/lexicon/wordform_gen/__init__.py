"""Одноразовая генерация словоформ из Stem. Не импортировать из runtime API."""

from .diminutives import generate_diminutive_forms
from .possessives import generate_possessive_forms
from .nouns import generate_noun_forms
from .verbs import generate_verb_forms

# Прилагательные: те же основы 0–5 и падежные окончания (именное склонение).
generate_adj_forms = generate_noun_forms

__all__ = [
    "generate_noun_forms",
    "generate_adj_forms",
    "generate_verb_forms",
    "generate_diminutive_forms",
    "generate_possessive_forms",
]
