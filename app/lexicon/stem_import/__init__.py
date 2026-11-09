"""
Одноразовый импорт основ из Word.orig.

Не импортировать из runtime-кода (API, models, serializers).
"""

from .build_stems import build_stems
from .parse_orig import ParsedOrig, parse_orig

__all__ = ["ParsedOrig", "parse_orig", "build_stems"]
