from __future__ import annotations

PUNCTUATION = ['.', ',', '?', '!', ';', "'", '(', ')', '_', '-', '[', ']']
REDUNDANT_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'but', 'by', 'for', 'from',
    'if', 'in', 'into', 'is', 'it', 'no', 'not', 'of', 'on', 'or', 'such',
    'that', 'the', 'their', 'then', 'there', 'these', 'they', 'this', 'to',
    'was', 'will', 'with', 'me', 'i', 'he', 'she', 'we', 'them', 'us',
}


def preprocess_text(text: str) -> str:
    cleaned = ''.join(ch for ch in text if ch not in PUNCTUATION)
    words = cleaned.split()
    normalized = [w.lower() if w.lower() not in {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'} else w for w in words]
    filtered = [w for w in normalized if w.lower() not in REDUNDANT_WORDS]
    return ' '.join(filtered)
