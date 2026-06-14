"""Configuration de l'application Django ``acronyme``."""

from django.apps import AppConfig


class AcronymeAppConfig(AppConfig):
    """Classe de configuration de l'application ``acronyme``.

    Référencée par défaut via ``INSTALLED_APPS = [..., 'acronyme']`` dans
    :mod:`config.settings`. Django utilise cette classe pour charger
    automatiquement l'application sans avoir à pointer explicitement vers
    ``acronyme.apps.AcronymeAppConfig``.

    Attributes:
        default_auto_field: Type de clé primaire auto-générée par défaut
            pour les modèles de l'application (``BigAutoField``).
        name: Nom Python du package de l'application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acronyme'
