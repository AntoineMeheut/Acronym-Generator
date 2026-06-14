"""Tests des routes URL de l'application ``acronyme``.

Vérifient à la fois :func:`django.urls.resolve` (URL → nom de vue) et
:func:`django.urls.reverse` (nom de vue → URL) pour les deux routes
``home`` et ``acronyme``.
"""

from django.urls import resolve, reverse


def test_home_url_resolves_to_home_view():
    match = resolve('/')
    assert match.view_name == 'home'


def test_acronyme_url_resolves_to_acronyme_view():
    match = resolve('/acronyme/')
    assert match.view_name == 'acronyme'


def test_home_url_reverses():
    assert reverse('home') == '/'


def test_acronyme_url_reverses():
    assert reverse('acronyme') == '/acronyme/'
