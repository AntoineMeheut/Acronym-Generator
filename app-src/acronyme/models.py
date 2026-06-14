"""Modèles Django de l'application ``acronyme``.

Le générateur ne persiste actuellement aucune donnée : toutes les listes
sont des constantes Python du package :mod:`resources`. Ce module est
conservé pour respecter la structure standard d'une app Django et accueillir
de futurs modèles si l'application est étendue (par exemple pour mémoriser
les acronymes générés).
"""

from django.db import models  # noqa: F401
