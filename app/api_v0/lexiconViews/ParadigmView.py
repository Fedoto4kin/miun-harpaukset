from collections import OrderedDict

from rest_framework.response import Response
from rest_framework.views import APIView

from lexicon.models import Word, WordForm


class ParadigmView(APIView):
    """Матрица словоформ леммы для попапа словаря."""

    def get(self, request, word_id, *args, **kwargs):
        try:
            word = Word.objects.select_related("pos").get(pk=word_id)
        except Word.DoesNotExist:
            return Response({"detail": "Not found"}, status=404)

        rows = (
            WordForm.objects.filter(word=word)
            .select_related("grammar_form")
            .order_by("grammar_form__sort_order", "id")
        )

        # Склеиваем альтернативы одного слота: "vezin / vezilöin"
        grouped = OrderedDict()
        for wf in rows:
            code = wf.grammar_form.code
            if code not in grouped:
                grouped[code] = {
                    "code": code,
                    "name_krl": wf.grammar_form.name_krl,
                    "name_ru": wf.grammar_form.name_ru,
                    "forms": [],
                    "number": (
                        "pl"
                        if ("_pl_" in code or code.endswith("_pl"))
                        else "sg"
                    ),
                }
            if wf.form not in grouped[code]["forms"]:
                grouped[code]["forms"].append(wf.form)

        forms = [
            {
                "code": g["code"],
                "name_krl": g["name_krl"],
                "name_ru": g["name_ru"],
                "form": " / ".join(g["forms"]),
                "number": g["number"],
            }
            for g in grouped.values()
        ]

        return Response(
            {
                "word_id": word.id,
                "lemma": word.word_clean,
                "pos": word.pos.abbr,
                "forms": forms,
            }
        )
