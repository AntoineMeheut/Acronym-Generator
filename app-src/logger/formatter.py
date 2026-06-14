"""module logger formatter"""
import logging
from datetime import datetime

import json

# Attributs pour le JsonFormatter
# Pour plus d'attributs consulter https://docs.python.org/3/library/logging.html#logrecord-attributes
# Attributs non sélectionnés : exc_info, levelno, msecs, msg, relativeCreated, stack_info, taskName
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
# Les attribus non sélectionnés
EXCLUDED_ATTRIBUTES = ['exc_text', 'exc_info', 'levelno', 'msecs', 'msg', 'relativeCreated', 'stack_info', 'taskName']

# Attributs custom java logger
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
    """Classe de formatter logging en json"""
    custom_format = None
    
    #@staticmethod
    def set_custom_attributes(self, attributes_dict):
        """méthode qui permet de surcharger le formatteur par un dictionnaire des attributs
        :param attributes_dict: dictionnaire contenant la clé à afficher et son attribut correspondant dans record
        """
        self.custom_format = attributes_dict
    

    def format(self, record):
        """méthode de formattage du code
        :param record: log récupéré
        :return: method to_json avec le record transformé
        """
        message = record.getMessage()      
        if self.custom_format is not None and len(self.custom_format) != 0 :
            fields = custom_fields(record.__dict__, self.custom_format)
            json_record = self.json_record(message, fields, record)
            #order attributes
            json_record = order_record(json_record, self.custom_format)
            # extra attribute
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
        """méthode de transformation en json
        :param record: log recupéré
        :return: dump du record
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
        """méthode de récupération des extras
        :param record: log recupéré
        :return: dict des extras
        """
        return {
            attr_name: record.__dict__[attr_name]
            for attr_name in record.__dict__
            if attr_name in RECORD_ATTRIBUTES or attr_name not in EXCLUDED_ATTRIBUTES
        }

    @staticmethod
    def custom_record(record_dict, custom_attributes):
        """méthode de récupération des extras
        :param custom_attributes dictionnaire
        :return: dict des extras
        """
        result_dict = {}
        for attr_name in custom_attributes:
            if custom_attributes[attr_name] in record_dict and record_dict[custom_attributes[attr_name]] is not None :
                result_dict[custom_attributes[attr_name]] = record_dict[custom_attributes[attr_name]]
        return result_dict
       
    @staticmethod
    def order_record(record_dict, custom_attributes):
        """méthode de récupération des extras
        :param custom_attributes dictionnaire
        :return: dict des extras
        """
        result_dict = {}
        for attr_name in custom_attributes:
            if custom_attributes[attr_name] in record_dict :
                result_dict[attr_name] = record_dict[custom_attributes[attr_name]]
        return result_dict
        
    def json_record(self, message, extra, record):
        """création du log complet
        :param message: message recupéré
        :param extra: extra recupéré
        :param record: record recupéré
        :return: l'extra modifié
        """
        extra['message'] = message
        if 'time' not in extra:
            extra['time'] = datetime.utcnow()
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)

        return extra


        
    @staticmethod
    def mutate_json_record(json_record):
        """transformation du json
        :param json_record: json transformé
        :return: le json modifié
        """
        for attr_name in json_record:
            attr = json_record[attr_name]
            if isinstance(attr, datetime):
                json_record[attr_name] = attr.isoformat()
        return json_record
        

class LegacyFormatter(logging.Formatter):
    """Classe de formatter logging en json"""

    def format(self, record):
        """méthode de formattage du code
        :param record: log récupéré
        :return: method to_json avec le record transformé
        """
        message = record.getMessage()
        fields = custom_fields(record.__dict__, LEGACY_ATTRIBUTES)
        json_record = self.format_fields(message, fields, record)
        #order attributes
        json_record = order_record(json_record, LEGACY_ATTRIBUTES)
        # extra attribute
        extra_att = custom_extra_fields(record)
        json_record = {**json_record, **extra_att}
        mutated_record = mutate_json_record(json_record)
        if mutated_record is None:
            mutated_record = json_record
        return to_json(mutated_record)
        

    def format_fields(self, message, extra, record):
        """création du log complet
        :param message: message recupéré
        :param extra: extra recupéré
        :param record: record recupéré
        :return: l'extra modifié
        """
        extra['message'] = message
        if 'time' not in extra:
            extra['time'] = datetime.utcnow()
        if record.exc_info:
            extra['exc_info'] = self.formatException(record.exc_info)
    
        return extra        


def _json_serializable(obj):
    """serialisation de l'object. On récupère soit le dict soit l'objet en str.
    """
    try:
        return obj.__dict__
    except AttributeError:
        return str(obj)


def to_json(record):
    """méthode de transformation en json
    :param record: log recupéré
    :return: dump du record
    """
    try:
        return json.dumps(record, default=_json_serializable)
    except (TypeError, ValueError, OverflowError):
        try:
            return json.dumps(record)
        except (TypeError, ValueError, OverflowError):
            return '{}'
            

def custom_extra_fields(record):
    """méthode de récupération des extras
    :param record: log recupéré
    :return: dict des extras
    """
    return {
        attr_name: record.__dict__[attr_name]
        for attr_name in record.__dict__
        if attr_name not in RECORD_ATTRIBUTES and attr_name not in EXCLUDED_ATTRIBUTES
    }
    

def custom_fields(record_dict, custom_attributes):
    """méthode de récupération des extras
    :param custom_attributes dictionnaire
    :return: dict des extras
    """
    result_dict = {}
    for attr_name in custom_attributes:
        if custom_attributes[attr_name] in record_dict and record_dict[custom_attributes[attr_name]] is not None :
            result_dict[custom_attributes[attr_name]] = record_dict[custom_attributes[attr_name]]
    return result_dict
    
    
def order_record(record_dict, custom_attributes):
    """méthode de récupération des extras
    :param custom_attributes dictionnaire
    :return: dict des extras
    """
    result_dict = {}
    for attr_name in custom_attributes:
        if custom_attributes[attr_name] in record_dict :
            result_dict[attr_name] = record_dict[custom_attributes[attr_name]]
    return result_dict
    

def mutate_json_record(json_record):
    """transformation du json
    :param json_record: json transformé
    :return: le json modifié
    """
    for attr_name in json_record:
        attr = json_record[attr_name]
        if isinstance(attr, datetime):
            json_record[attr_name] = attr.isoformat()
    return json_record
   
   
    