"""Formatters de logs au format JSON.

Fournit deux classes prêtes à l'emploi pour la configuration ``LOGGING``
de Django :

- :class:`JsonFormatter` — schéma de sortie standard, basé sur les
  attributs natifs de :class:`logging.LogRecord`. Peut être surchargé via
  :meth:`JsonFormatter.set_custom_attributes` pour renommer ou réordonner
  les clés.
- :class:`LegacyFormatter` — schéma de sortie aligné sur la convention
  « legacy Java » (``severity``, ``loggerName``, ``threadId``…), pratique
  pour interopérer avec des pipelines de logs existants.

Les deux classes :

- conservent les *extras* non standard ajoutés sur l'enregistrement
  (``record.user_id = 42`` → clé ``user_id`` dans le JSON) ;
- sérialisent les exceptions via :meth:`logging.Formatter.formatException` ;
- convertissent automatiquement les :class:`~datetime.datetime` en chaînes
  ISO 8601 ;
- retombent sur une chaîne JSON minimale en cas d'erreur de sérialisation.

Pour la liste complète des attributs de ``LogRecord``, voir la
documentation Python :
https://docs.python.org/3/library/logging.html#logrecord-attributes
"""

import logging
from datetime import datetime

import json

# Attributs natifs de LogRecord exposés dans le JSON.
# Les attributs hors de cet ensemble (s'ils ne sont pas explicitement exclus)
# sont considérés comme des extras et également ajoutés à la sortie.
RECORD_ATTRIBUTES = {
    'args',
    'asctime',
    'created',
    'filename',
    'funcName',
    'levelname',
    'lineno',
    'message',
    'module',
    'name',
    'pathname',
    'process',
    'processName',
    'thread',
    'threadName',
}

# Attributs natifs explicitement écartés du JSON (bruit ou doublons).
EXCLUDED_ATTRIBUTES = ['exc_text', 'exc_info', 'levelno', 'msecs', 'msg', 'relativeCreated', 'stack_info', 'taskName']

# Mapping {clé_sortie: attribut_LogRecord} utilisé par LegacyFormatter
# pour produire un schéma de logs « style Java ».
LEGACY_ATTRIBUTES = {
	'timestamp': 'time',
	'message': 'message',
	'exception': 'exc_info',
	'severity': 'levelname',
	'package': 'module',
	'method': 'funcName',
	'line': 'lineno',
	'file': 'filename',
	'loggerName': 'name',
	'threadName': 'threadName',
	'threadId': 'thread',
}

CUSTOM_ATTRIBUTES = {}


class JsonFormatter(logging.Formatter):
    """Formatter de logs produisant un objet JSON par enregistrement.

    Par défaut, la sortie reprend les attributs natifs de
    :class:`logging.LogRecord` (cf. :data:`RECORD_ATTRIBUTES`) plus les
    extras déposés sur l'enregistrement. Le schéma peut être personnalisé
    via :meth:`set_custom_attributes` : on fournit un mapping
    ``{clé_sortie: attribut_LogRecord}`` et le formatter renomme/réordonne
    les champs en conséquence (les extras restent ajoutés à la fin).
    """

    custom_format = None

    def set_custom_attributes(self, attributes_dict):
        """Surcharge le schéma de sortie du formatter.

        Args:
            attributes_dict: Mapping ``{clé_sortie: attribut_LogRecord}``.
                L'ordre des clés est respecté dans le JSON produit.
        """
        self.custom_format = attributes_dict

    def format(self, record):
        """Formatte un enregistrement de log en chaîne JSON.

        Args:
            record: Enregistrement à formater.

        Returns:
            La représentation JSON (str) de l'enregistrement.
        """
        message = record.getMessage()
        if self.custom_format is not None and len(self.custom_format) != 0 :
            fields = custom_fields(record.__dict__, self.custom_format)
            json_record = self.json_record(message, fields, record)
            json_record = order_record(json_record, self.custom_format)
            extra_att = custom_extra_fields(record)
            json_record = {**json_record, **extra_att}
        else :
            extra = self.extra_from_record(record)
            json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    @staticmethod
    def to_json(record):
        """Sérialise un dictionnaire en chaîne JSON.

        Args:
            record: Dictionnaire à sérialiser.

        Returns:
            La chaîne JSON. Retombe sur ``'{}'`` en cas d'échec.
        """
        try:
            return json.dumps(record, default=_json_serializable)
        except (TypeError, ValueError, OverflowError):
            try:
                return json.dumps(record)
            except (TypeError, ValueError, OverflowError):
                return '{}'

    @staticmethod
    def extra_from_record(record):
        """Extrait les attributs à exposer en sortie depuis un ``LogRecord``.

        Inclut les attributs natifs listés dans :data:`RECORD_ATTRIBUTES`
        ainsi que tous les extras non explicitement exclus.

        Args:
            record: Enregistrement source.

        Returns:
            Dictionnaire ``{attribut: valeur}``.
        """
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name in RECORD_ATTRIBUTES or attr_name not in EXCLUDED_ATTRIBUTES
        }

    @staticmethod
    def custom_record(record_dict, custom_attributes):
        """Filtre un dictionnaire selon un mapping d'attributs custom.

        Args:
            record_dict: Dictionnaire source (typiquement
                ``record.__dict__``).
            custom_attributes: Mapping
                ``{clé_sortie: attribut_LogRecord}``.

        Returns:
            Dictionnaire ne contenant que les attributs présents et non
            ``None`` dans la source.
        """
        result_dict = {}
        for attr_name in custom_attributes:
            if custom_attributes[attr_name] in record_dict and record_dict[custom_attributes[attr_name]] is not None :
                result_dict[custom_attributes[attr_name]] = record_dict[custom_attributes[attr_name]]
        return result_dict

    @staticmethod
    def order_record(record_dict, custom_attributes):
        """Renomme et réordonne un dictionnaire selon un mapping custom.

        Args:
            record_dict: Dictionnaire source (clés = attributs LogRecord).
            custom_attributes: Mapping
                ``{clé_sortie: attribut_LogRecord}``. L'ordre des clés
                du mapping est respecté.

        Returns:
            Dictionnaire avec les clés renommées et réordonnées.
        """
        result_dict = {}
        for attr_name in custom_attributes:
            if custom_attributes[attr_name] in record_dict :
                result_dict[attr_name] = record_dict[custom_attributes[attr_name]]
        return result_dict

    def json_record(self, message, extra, record):
        """Construit le dictionnaire JSON final pour un enregistrement.

        Ajoute systématiquement la clé ``message`` et — si absente — la
        clé ``time`` (UTC). Sérialise l'exception éventuelle dans
        ``exc_info``.

        Args:
            message: Message déjà formaté de l'enregistrement.
            extra: Dictionnaire de base à enrichir.
            record: Enregistrement source.

        Returns:
            Dictionnaire enrichi prêt à être sérialisé en JSON.
        """
        extra['message'] = message
        if 'time' not in extra:
            extra['time'] = datetime.utcnow()
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra

    @staticmethod
    def mutate_json_record(json_record):
        """Convertit les valeurs ``datetime`` en chaînes ISO 8601.

        Args:
            json_record: Dictionnaire à transformer en place.

        Returns:
            Le même dictionnaire, avec les ``datetime`` remplacés par leur
            représentation ISO.
        """
        for attr_name in json_record:
            attr = json_record[attr_name]
            if isinstance(attr, datetime):
                json_record[attr_name] = attr.isoformat()
        return json_record


class LegacyFormatter(logging.Formatter):
    """Formatter de logs au schéma « legacy Java » (``severity``, ``loggerName``…).

    Utilise systématiquement :data:`LEGACY_ATTRIBUTES` pour mapper les
    attributs natifs de ``LogRecord`` vers les clés de sortie attendues
    par des pipelines de logs Java/historiques. Les extras déposés sur
    l'enregistrement sont conservés tels quels dans le JSON.
    """

    def format(self, record):
        """Formatte un enregistrement de log en chaîne JSON « legacy ».

        Args:
            record: Enregistrement à formater.

        Returns:
            La représentation JSON (str) de l'enregistrement.
        """
        message = record.getMessage()
        fields = custom_fields(record.__dict__, LEGACY_ATTRIBUTES)
        json_record = self.format_fields(message, fields, record)
        json_record = order_record(json_record, LEGACY_ATTRIBUTES)
        extra_att = custom_extra_fields(record)
        json_record = {**json_record, **extra_att}
        mutated_record = mutate_json_record(json_record)
        if mutated_record is None:
            mutated_record = json_record
        return to_json(mutated_record)

    def format_fields(self, message, extra, record):
        """Construit le dictionnaire JSON final pour un enregistrement legacy.

        Ajoute systématiquement la clé ``message`` et — si absente — la
        clé ``time`` (UTC). Sérialise l'exception éventuelle dans
        ``exc_info``.

        Args:
            message: Message déjà formaté de l'enregistrement.
            extra: Dictionnaire de base à enrichir.
            record: Enregistrement source.

        Returns:
            Dictionnaire enrichi prêt à être réordonné puis sérialisé.
        """
        extra['message'] = message
        if 'time' not in extra:
            extra['time'] = datetime.utcnow()
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra


def _json_serializable(obj):
    """Fonction de fallback pour :func:`json.dumps`.

    Retourne ``obj.__dict__`` si l'objet l'expose, sinon sa représentation
    ``str(obj)``. Permet de sérialiser des instances de classes
    arbitraires sans :class:`json.JSONEncoder` dédié.

    Args:
        obj: Objet à sérialiser.

    Returns:
        Valeur JSON-compatible (``dict`` ou ``str``).
    """
    try:
        return obj.__dict__
    except AttributeError:
        return str(obj)


def to_json(record):
    """Sérialise un dictionnaire en chaîne JSON (variante module-level).

    Args:
        record: Dictionnaire à sérialiser.

    Returns:
        La chaîne JSON. Retombe sur ``'{}'`` en cas d'échec.
    """
    try:
        return json.dumps(record, default=_json_serializable)
    except (TypeError, ValueError, OverflowError):
        try:
            return json.dumps(record)
        except (TypeError, ValueError, OverflowError):
            return '{}'


def custom_extra_fields(record):
    """Extrait les *extras* non standard d'un ``LogRecord``.

    Args:
        record: Enregistrement source.

    Returns:
        Dictionnaire des attributs qui ne sont ni des attributs natifs
        listés dans :data:`RECORD_ATTRIBUTES`, ni explicitement exclus.
    """
    return {
        attr_name: record.__dict__[attr_name]
        for attr_name in record.__dict__
        if attr_name not in RECORD_ATTRIBUTES and attr_name not in EXCLUDED_ATTRIBUTES
    }


def custom_fields(record_dict, custom_attributes):
    """Filtre un dictionnaire selon un mapping d'attributs custom.

    Variante module-level utilisée par :class:`LegacyFormatter`.

    Args:
        record_dict: Dictionnaire source (typiquement ``record.__dict__``).
        custom_attributes: Mapping ``{clé_sortie: attribut_LogRecord}``.

    Returns:
        Dictionnaire ne contenant que les attributs présents et non
        ``None`` dans la source.
    """
    result_dict = {}
    for attr_name in custom_attributes:
        if custom_attributes[attr_name] in record_dict and record_dict[custom_attributes[attr_name]] is not None :
            result_dict[custom_attributes[attr_name]] = record_dict[custom_attributes[attr_name]]
    return result_dict


def order_record(record_dict, custom_attributes):
    """Renomme et réordonne un dictionnaire selon un mapping custom.

    Variante module-level utilisée par :class:`LegacyFormatter`.

    Args:
        record_dict: Dictionnaire source (clés = attributs LogRecord).
        custom_attributes: Mapping ``{clé_sortie: attribut_LogRecord}``.

    Returns:
        Dictionnaire avec les clés renommées et réordonnées selon le
        mapping fourni.
    """
    result_dict = {}
    for attr_name in custom_attributes:
        if custom_attributes[attr_name] in record_dict :
            result_dict[attr_name] = record_dict[custom_attributes[attr_name]]
    return result_dict


def mutate_json_record(json_record):
    """Convertit les valeurs ``datetime`` en chaînes ISO 8601.

    Variante module-level utilisée par :class:`LegacyFormatter`.

    Args:
        json_record: Dictionnaire à transformer en place.

    Returns:
        Le même dictionnaire, avec les ``datetime`` remplacés par leur
        représentation ISO.
    """
    for attr_name in json_record:
        attr = json_record[attr_name]
        if isinstance(attr, datetime):
            json_record[attr_name] = attr.isoformat()
    return json_record
