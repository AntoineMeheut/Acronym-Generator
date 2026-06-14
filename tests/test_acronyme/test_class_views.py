"""Tests des vues ``home`` et ``acronyme_page`` en style
:class:`django.test.SimpleTestCase`.

Doublon volontaire de :mod:`tests.test_acronyme.test_views` (qui utilise
le style fonctionnel ``pytest``) : ce module garantit que les vues
restent compatibles avec le runner ``manage.py test`` standard de
Django, en plus de ``pytest``.
"""

from django.test import SimpleTestCase
from django.urls import reverse

from resources.initlist import GROS_MOTS


class HomePageTest(SimpleTestCase):
    def test_home_renders_nav(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bienvenue')
        self.assertContains(response, 'Outils')
        self.assertContains(response, 'Acronyme')


class AcronymePageTest(SimpleTestCase):
    def test_combo_lists_every_word(self):
        response = self.client.get(reverse('acronyme'))
        for word in GROS_MOTS:
            self.assertContains(response, word)

    def test_selecting_known_word_displays_letter_choices(self):
        response = self.client.get(reverse('acronyme'), {'word': 'BORDEL'})
        self.assertContains(response, 'Mot sélectionné')
        # 6 letters
        self.assertEqual(response.content.count(b'<div class="letter-badge">'), 6)

    def test_unknown_word_ignored(self):
        response = self.client.get(reverse('acronyme'), {'word': 'xyz'})
        self.assertNotContains(response, 'Mot sélectionné')

    def test_full_letter_choices_render_sentence(self):
        response = self.client.get(reverse('acronyme'), {
            'word': 'NUL',
            'letter_0': 'Négociation',
            'letter_1': 'Unité',
            'letter_2': 'Leadership',
        })
        self.assertContains(response, 'Résultat')
        self.assertContains(response, 'Négociation Unité Leadership')
