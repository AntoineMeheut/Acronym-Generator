from django.urls import reverse

from resources.initlist import GROS_MOTS


def test_home_page_renders(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert b'Bienvenue' in response.content
    assert b'Outils' in response.content


def test_acronyme_page_without_word_shows_menu_only(client):
    response = client.get(reverse('acronyme'))
    assert response.status_code == 200
    for word in GROS_MOTS:
        assert word.encode() in response.content
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content
    assert b'<div class="letter-badge">' not in response.content


def test_acronyme_page_select_known_word_shows_letter_dropdowns(client):
    response = client.get(reverse('acronyme'), {'word': 'MERDE'})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' in response.content
    # MERDE has 5 letters → 5 badges
    assert response.content.count(b'<div class="letter-badge">') == 5
    assert b'>M<' in response.content
    assert b'>E<' in response.content
    assert b'>R<' in response.content
    assert b'>D<' in response.content


def test_acronyme_page_select_unknown_word_ignored(client):
    response = client.get(reverse('acronyme'), {'word': 'inconnu'})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content
    assert b'<div class="letter-badge">' not in response.content


def test_acronyme_page_word_is_case_insensitive(client):
    response = client.get(reverse('acronyme'), {'word': 'merde'})
    assert response.status_code == 200
    assert b'MERDE' in response.content
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' in response.content


def test_acronyme_page_empty_word_treated_as_none(client):
    response = client.get(reverse('acronyme'), {'word': ''})
    assert response.status_code == 200
    assert b'Mot s\xc3\xa9lectionn\xc3\xa9' not in response.content


def test_acronyme_page_partial_letter_choices_no_sentence(client):
    response = client.get(reverse('acronyme'), {
        'word': 'MERDE',
        'letter_0': 'Management',
    })
    assert response.status_code == 200
    assert b'R\xc3\xa9sultat' not in response.content


def test_acronyme_page_invalid_letter_choice_dropped(client):
    response = client.get(reverse('acronyme'), {
        'word': 'MERDE',
        'letter_0': 'NotARealWord',
        'letter_1': 'Excellence',
        'letter_2': 'Reporting',
        'letter_3': 'Direction',
        'letter_4': 'Engagement',
    })
    assert response.status_code == 200
    # letter_0 was invalid → no sentence
    assert b'R\xc3\xa9sultat' not in response.content


def test_acronyme_page_all_letter_choices_renders_sentence(client):
    response = client.get(reverse('acronyme'), {
        'word': 'MERDE',
        'letter_0': 'Management',
        'letter_1': 'Excellence',
        'letter_2': 'Reporting',
        'letter_3': 'Direction',
        'letter_4': 'Engagement',
    })
    assert response.status_code == 200
    assert b'R\xc3\xa9sultat' in response.content
    assert b'Management Excellence Reporting Direction Engagement' in response.content


def test_acronyme_page_preserves_chosen_letter_in_select(client):
    response = client.get(reverse('acronyme'), {
        'word': 'MERDE',
        'letter_0': 'Management',
    })
    assert b'value="Management" selected' in response.content


def test_acronyme_page_short_word_has_correct_badge_count(client):
    response = client.get(reverse('acronyme'), {'word': 'NUL'})
    assert response.content.count(b'<div class="letter-badge">') == 3


def test_acronyme_page_long_word_has_correct_badge_count(client):
    response = client.get(reverse('acronyme'), {'word': 'PUTAIN'})
    assert response.content.count(b'<div class="letter-badge">') == 6
