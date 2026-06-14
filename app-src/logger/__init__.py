"""Package ``logger`` — formatters de logs in-tree.

Expose deux formatters de logs Python utilisables dans la configuration
``LOGGING`` de Django (:mod:`config.settings`) :

- :class:`logger.formatter.JsonFormatter` — formatte chaque enregistrement
  de log en JSON, avec possibilité de surcharge des attributs.
- :class:`logger.formatter.LegacyFormatter` — variante au schéma de
  nommage « legacy Java » (``severity``, ``loggerName``, ``threadId``…).
"""
