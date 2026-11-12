# wordform_gen — одноразовая генерация словоформ

Не часть runtime API. Правила имён — из `Grammatika_karelia_proper_tver.doc`
(фрагмент в `_grammatika_nouns.txt`).

```bash
python manage.py test lexicon.tests.test_wordform_gen
python manage.py generate_wordforms --pos=s. [--dry-run] [--limit N]
python manage.py generate_wordforms --pos=a. [--dry-run] [--limit N]
python manage.py generate_wordforms --pos=v. [--dry-run] [--limit N]
# отрицательный глагол ei (готовая таблица, не Stem):
python manage.py import_negation_verb [--dry-run]
# продуктивные уменьшительные s. на -ne (отдельная category; не в таблице парадигмы):
python manage.py generate_diminutives [--dry-run] [--limit N] [--word peldo]
# притяжательные -ni / -š (+ -zeni/-zeš; search-only):
python manage.py generate_possessives [--dry-run] [--limit N] [--word muamo]
# аудит основ s. (структура / Dictorpus) + точечный regen после книги:
python manage.py audit_stems --layer=1 --out /tmp/stems_l1.jsonl
python manage.py regen_lemma --word=rebo
# см. lexicon/stem_audit/README.md
```

Прилагательные (`a.`) — тот же генератор, что и имена (`generate_adj_forms` ≡ `generate_noun_forms`).

Глаголы (`v.`): фазы 1–2 — финитные + потенциал + инф. II–III + причастия + аналитика (на слоте 141).
Форма 73 (конд. имп. 3sg) — по блок-схеме `_grammatika_verb_cond73.png`.
