# wordform_gen — одноразовая генерация словоформ

Не часть runtime API. Правила имён — из `Grammatika_karelia_proper_tver.doc`
(фрагмент в `_grammatika_nouns.txt`).

```bash
python manage.py test lexicon.tests.test_wordform_gen
python manage.py generate_wordforms --pos=s. [--dry-run] [--limit N]
python manage.py generate_wordforms --pos=a. [--dry-run] [--limit N]
python manage.py generate_wordforms --pos=v. [--dry-run] [--limit N]
# продуктивные уменьшительные s. на -ne (отдельная category; не в таблице парадигмы):
python manage.py generate_diminutives [--dry-run] [--limit N] [--word peldo]
```

Прилагательные (`a.`) — тот же генератор, что и имена (`generate_adj_forms` ≡ `generate_noun_forms`).

Глаголы (`v.`): фазы 1–2 — финитные + потенциал + инф. II–III + причастия + аналитика (на слоте 141).
Форма 73 (конд. имп. 3sg) — по блок-схеме `_grammatika_verb_cond73.png`.
