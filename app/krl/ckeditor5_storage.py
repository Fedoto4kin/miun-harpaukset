import os
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class CKEditor5FileStorage(FileSystemStorage):
    """Keep uploads under MEDIA/uploads/ (same as old CKEDITOR_UPLOAD_PATH)."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", os.path.join(settings.MEDIA_ROOT, "uploads"))
        kwargs.setdefault("base_url", urljoin(settings.MEDIA_URL, "uploads/"))
        super().__init__(*args, **kwargs)
