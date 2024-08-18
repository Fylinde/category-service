# category-service/app/utils/slug_utils.py

import re
import unicodedata

def generate_slug(name: str) -> str:
    slug = unicodedata.normalize("NFKD", name)
    slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug
