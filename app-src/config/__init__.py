"""Projet Django ``acronyme``.

Ce package contient la configuration globale du projet :

- :mod:`config.settings` — paramètres Django (DB, INSTALLED_APPS, LOGGING…),
- :mod:`config.urls` — routes racine (inclut ``acronyme.urls`` et le schéma
  OpenAPI/Swagger via ``drf-spectacular``),
- :mod:`config.wsgi` et :mod:`config.asgi` — points d'entrée serveur.
"""
