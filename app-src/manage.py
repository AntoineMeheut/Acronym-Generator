#!/usr/bin/env python
"""Utilitaire en ligne de commande Django pour les tâches d'administration.

Lance les commandes ``manage.py`` standard (``runserver``, ``migrate``,
``check``, ``createsuperuser``…). Configure ``DJANGO_SETTINGS_MODULE`` sur
:mod:`config.settings` si la variable n'est pas déjà définie.

Usage (depuis ``app-src/``) :

    python manage.py runserver

Usage (depuis la racine du projet, avec le ``.env`` de démonstration) :

    ENV_PATH=app-src/.env.dist python app-src/manage.py runserver
"""

import os
import sys


def main():
    """Charge les paramètres Django puis exécute la commande demandée."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
