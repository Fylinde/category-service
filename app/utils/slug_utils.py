import re
import unicodedata
from typing import Optional
from slugify import slugify  # Optional: You can use a library like python-slugify for additional features.

# Optional: You can define a list of common stop words to remove from slugs.
STOP_WORDS = set(["the", "is", "in", "and", "a", "an", "on", "of", "with", "for", "at", "by", "from", "to"])

def generate_slug(name: str, remove_stopwords: bool = False, max_length: Optional[int] = None, delimiter: str = '-') -> str:
    """
    Generate a slug from a given string.
    
    :param name: The string from which to generate the slug.
    :param remove_stopwords: Whether to remove common stop words from the slug.
    :param max_length: Optional maximum length for the slug.
    :param delimiter: The delimiter to use in the slug (default is '-').
    :return: A clean slug version of the input string.
    """
    # Step 1: Normalize the string (Unicode normalization)
    slug = unicodedata.normalize("NFKD", name)
    
    # Step 2: Remove special characters, punctuation, and non-word characters
    slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
    
    # Step 3: Optionally remove common stop words
    if remove_stopwords:
        slug_words = [word for word in slug.split() if word not in STOP_WORDS]
        slug = " ".join(slug_words)
    
    # Step 4: Replace whitespace and consecutive delimiters with a single delimiter
    slug = re.sub(r'[-\s]+', delimiter, slug)

    # Step 5: Optionally limit the length of the slug
    if max_length:
        slug = slug[:max_length].rstrip(delimiter)

    return slug

# Example usage:
# slug = generate_slug("The Best Category Ever", remove_stopwords=True, max_length=30)
# Output: "best-category-ever"
