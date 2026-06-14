"""Tests de la vue :func:`acronyme.views.genauto_page`.

Couvre :

- rendu de la page sans mot (combo seule, pas de phrases) ;
- rendu avec un mot valide → 10 phrases, chaque mot commence par la
  lettre attendue ;
- mot inconnu ignoré ;
- normalisation case-insensitive du paramètre ``word``.
"""

import unicodedata

from django.urls import reverse

from resources.initlist import GROS_MOTS

SENTENCE_MARKER = b'<p class="sentence">'


def _strip_accents(value):
    normalized = unicodedata.normalize('NFD', value)
    return ''.join(c for c in normalized if not unicodedata.combining(c))


def _extract_sentences(content):
    parts = content.split(SENTENCE_MARKER)[1:]
    return [part.split(b'</p>', 1)[0].decode('utf-8') for part in parts]


def test_genauto_without_word_shows_combo_only(client):
    response = client.get(reverse('genauto'))
    assert response.status_code == 200
    for word in GROS_MOTS:
        assert word.encode() in response.content
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content
    assert SENTENCE_MARKER not in response.content


def test_genauto_with_valid_word_renders_ten_sentences(client):
    response = client.get(reverse('genauto'), {'word': 'MERDE'})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' in response.content
    sentences = _extract_sentences(response.content)
    assert len(sentences) == 10
    for sentence in sentences:
        words = sentence.split(' ')
        assert len(words) == 5
        for word, expected_letter in zip(words, 'MERDE'):
            first_letter = _strip_accents(word[0]).upper()
            assert first_letter == expected_letter


def test_genauto_with_unknown_word_ignored(client):
    response = client.get(reverse('genauto'), {'word': 'inconnu'})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content
    assert SENTENCE_MARKER not in response.content


def test_genauto_with_lowercase_word_is_normalized(client):
    response = client.get(reverse('genauto'), {'word': 'merde'})
    assert response.status_code == 200
    assert b'MERDE' in response.content
    sentences = _extract_sentences(response.content)
    assert len(sentences) == 10


def test_genauto_with_empty_word_treated_as_none(client):
    response = client.get(reverse('genauto'), {'word': ''})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content
    assert SENTENCE_MARKER not in response.content


def test_genauto_short_word_three_words_per_sentence(client):
    response = client.get(reverse('genauto'), {'word': 'NUL'})
    sentences = _extract_sentences(response.content)
    assert len(sentences) == 10
    for sentence in sentences:
        assert len(sentence.split(' ')) == 3
