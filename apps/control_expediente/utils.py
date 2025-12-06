# utils.py
import unicodedata
import os
from django.utils.text import slugify
from decimal import Decimal, InvalidOperation

def normalize_filename(filename):
    name, ext = os.path.splitext(filename)

    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    name = slugify(name)

    return f"{name}{ext.lower()}"


def to_decimal(value, default="0"):
    try:
        if value in [None, ""]:
            return Decimal(default)
        return Decimal(str(value).replace(",", "."))
    except (InvalidOperation, ValueError):
        return Decimal(default)