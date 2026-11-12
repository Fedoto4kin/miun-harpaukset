from django_ckeditor_5.widgets import CKEditor5Widget


class KrlCKEditor5Widget(CKEditor5Widget):
    """CKEditor 5 widget with Insert Badge helper for lesson HTML."""

    class Media:
        js = ("js/ckeditor5_insert_badge.js",)
