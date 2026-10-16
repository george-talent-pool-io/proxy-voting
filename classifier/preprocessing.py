"""Lossless source storage is separate from deterministic model preprocessing."""
import hashlib
import re
import unicodedata
from bs4 import BeautifulSoup

VERSION = 'nfc-html-whitespace-v1'

def source_hash(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError('Notice text must be a string')
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def normalise(text: str) -> str:
    source_hash(text)
    text = unicodedata.normalize('NFC', text)
    if re.search(r'<(?:!doctype|/?[a-zA-Z][^>]*>)', text):
        soup = BeautifulSoup(text, 'html.parser')
        for el in soup(['script', 'style']):
            el.decompose()
        text = soup.get_text(' ')
    return re.sub(r'\s+', ' ', text).strip()

def shingles(text: str) -> set[str]:
    # Mask dates/numbers for conservative template grouping, never for model inputs.
    words = re.findall(r'\w+', re.sub(r'\d+', '#', normalise(text).casefold()))
    return {' '.join(words[i:i+5]) for i in range(max(1, len(words)-4))}
