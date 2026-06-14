"""Routes URL de l'application ``acronyme``.

Deux routes sont exposées :

- ``''`` → :func:`acronyme.views.home`, page d'accueil (nom ``home``),
- ``'acronyme/'`` → :func:`acronyme.views.acronyme_page`, page de génération
  de l'acronyme (nom ``acronyme``).

Ces routes sont incluses depuis :mod:`config.urls` au préfixe racine.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('acronyme/', views.acronyme_page, name='acronyme'),
]
