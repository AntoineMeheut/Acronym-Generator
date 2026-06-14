"""Routes URL de l'application ``acronyme``.

Trois routes sont exposées :

- ``''`` → :func:`acronyme.views.home`, page d'accueil (nom ``home``),
- ``'acronyme/'`` → :func:`acronyme.views.acronyme_page`, page de
  génération manuelle d'acronyme (nom ``acronyme``),
- ``'genauto/'`` → :func:`acronyme.views.genauto_page`, page de génération
  automatique de 10 acronymes (nom ``genauto``).

Ces routes sont incluses depuis :mod:`config.urls` au préfixe racine.
"""

from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('acronyme/', views.acronyme_page, name='acronyme'),
    path('genauto/', views.genauto_page, name='genauto'),
]
