"""Configuration de l'application."""


from django.apps import AppConfig


class AcronymeAppConfig(AppConfig):
    """
    Sert à indiquer à Django comment charger automatiquement la configuration lorsque INSTALLED_APPS contient le chemin vers le module principal d’une application plutôt que le chemin vers sa classe de configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'acronyme'
