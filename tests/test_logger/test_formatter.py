"""Tests de :mod:`logger.formatter`.

Trois sections :

- ``JsonFormatter`` — schéma standard, surcharge via
  ``set_custom_attributes``, helpers de classe (``to_json``,
  ``extra_from_record``, ``custom_record``, ``order_record``,
  ``mutate_json_record``, ``json_record``).
- ``LegacyFormatter`` — schéma legacy Java, support des exceptions et
  des extras non standard.
- Helpers module-level — ``_json_serializable``, ``to_json``,
  ``custom_fields``, ``order_record``, ``custom_extra_fields``,
  ``mutate_json_record``.
"""

import json
import logging
import sys
from datetime import datetime

from logger.formatter import (
    JsonFormatter,
    LegacyFormatter,
    _json_serializable,
    custom_extra_fields,
    custom_fields,
    mutate_json_record,
    order_record,
    to_json,
)


def _make_record(msg='hello', name='test.logger', level=logging.INFO):
    return logging.LogRecord(
        name=name,
        level=level,
        pathname=__file__,
        lineno=10,
        msg=msg,
        args=None,
        exc_info=None,
    )


def _make_record_with_exc(msg='oops', exc_type=ValueError, exc_msg='boom'):
    try:
        raise exc_type(exc_msg)
    except exc_type:
        exc_info = sys.exc_info()
    return logging.LogRecord(
        name='x', level=logging.ERROR, pathname=__file__, lineno=1,
        msg=msg, args=None, exc_info=exc_info,
    )


# ---------- JsonFormatter ----------

def test_json_formatter_format_basic_fields():
    record = _make_record('hello')
    out = JsonFormatter().format(record)
    data = json.loads(out)
    assert data['message'] == 'hello'
    assert data['levelname'] == 'INFO'
    assert data['name'] == 'test.logger'
    assert 'time' in data


def test_json_formatter_format_includes_exc_info_when_present():
    record = _make_record_with_exc('oops')
    data = json.loads(JsonFormatter().format(record))
    assert 'exc_info' in data
    assert 'ValueError' in data['exc_info']
    assert 'boom' in data['exc_info']


def test_json_formatter_custom_format_renames_keys():
    record = _make_record('hi')
    f = JsonFormatter()
    f.set_custom_attributes({'severity': 'levelname', 'msg': 'message'})
    data = json.loads(f.format(record))
    assert data['severity'] == 'INFO'
    assert data['msg'] == 'hi'


def test_json_formatter_custom_format_includes_extras():
    record = _make_record('hi')
    record.user_id = 123
    f = JsonFormatter()
    f.set_custom_attributes({'severity': 'levelname'})
    data = json.loads(f.format(record))
    assert data['user_id'] == 123


def test_json_formatter_to_json_handles_simple_record():
    out = JsonFormatter.to_json({'a': 1, 'b': 'x'})
    assert json.loads(out) == {'a': 1, 'b': 'x'}


def test_json_formatter_extra_from_record_includes_standard_fields():
    record = _make_record('hi')
    record.user_id = 42
    extras = JsonFormatter.extra_from_record(record)
    assert extras['levelname'] == 'INFO'
    assert extras['user_id'] == 42


def test_json_formatter_custom_record_static_method():
    record_dict = {'message': 'hi', 'levelname': 'INFO'}
    result = JsonFormatter.custom_record(record_dict, {'msg': 'message', 'lvl': 'levelname'})
    assert result == {'message': 'hi', 'levelname': 'INFO'}


def test_json_formatter_order_record_static_method():
    record_dict = {'message': 'hi', 'levelname': 'INFO'}
    result = JsonFormatter.order_record(record_dict, {'msg': 'message', 'severity': 'levelname'})
    assert list(result.keys()) == ['msg', 'severity']
    assert result == {'msg': 'hi', 'severity': 'INFO'}


def test_json_formatter_mutate_converts_datetime():
    dt = datetime(2026, 1, 1, 12, 0, 0)
    result = JsonFormatter.mutate_json_record({'time': dt, 'msg': 'hi'})
    assert result['time'] == dt.isoformat()
    assert result['msg'] == 'hi'


def test_json_formatter_json_record_adds_message_and_time():
    record = _make_record('hi')
    f = JsonFormatter()
    out = f.json_record('hi', {}, record)
    assert out['message'] == 'hi'
    assert 'time' in out


def test_json_formatter_json_record_preserves_existing_time():
    record = _make_record('hi')
    existing = datetime(2020, 1, 1)
    out = JsonFormatter().json_record('hi', {'time': existing}, record)
    assert out['time'] == existing


# ---------- LegacyFormatter ----------

def test_legacy_formatter_basic_fields():
    record = _make_record('legacy')
    data = json.loads(LegacyFormatter().format(record))
    assert data['message'] == 'legacy'
    assert data['severity'] == 'INFO'
    assert 'timestamp' in data
    assert data['loggerName'] == 'test.logger'


def test_legacy_formatter_with_exception():
    record = _make_record_with_exc('legacy oops', exc_type=RuntimeError, exc_msg='kaboom')
    data = json.loads(LegacyFormatter().format(record))
    assert 'exception' in data
    assert 'RuntimeError' in data['exception']
    assert 'kaboom' in data['exception']


def test_legacy_formatter_includes_extra_fields():
    record = _make_record('legacy')
    record.custom_field = 'custom_value'
    data = json.loads(LegacyFormatter().format(record))
    assert data['custom_field'] == 'custom_value'


def test_legacy_formatter_format_fields_method():
    record = _make_record('hi')
    f = LegacyFormatter()
    out = f.format_fields('hi', {}, record)
    assert out['message'] == 'hi'
    assert 'time' in out


def test_legacy_formatter_format_fields_preserves_time():
    record = _make_record('hi')
    existing = datetime(2020, 1, 1)
    out = LegacyFormatter().format_fields('hi', {'time': existing}, record)
    assert out['time'] == existing


# ---------- Module-level helpers ----------

def test_json_serializable_uses_dict_when_available():
    class A:
        def __init__(self):
            self.x = 5
    assert _json_serializable(A()) == {'x': 5}


def test_json_serializable_falls_back_to_str_when_no_dict():
    class B:
        __slots__ = ()
    out = _json_serializable(B())
    assert isinstance(out, str)


def test_to_json_serializes_dict():
    assert json.loads(to_json({'a': 1})) == {'a': 1}


def test_to_json_handles_object_with_dict_via_default():
    class A:
        def __init__(self):
            self.x = 5
    out = to_json({'obj': A()})
    assert json.loads(out) == {'obj': {'x': 5}}


def test_custom_fields_returns_only_present_keys():
    record_dict = {'message': 'hi', 'levelname': 'INFO'}
    result = custom_fields(record_dict, {'msg': 'message', 'lvl': 'levelname', 'gone': 'absent'})
    assert result == {'message': 'hi', 'levelname': 'INFO'}


def test_custom_fields_skips_none_values():
    record_dict = {'message': None, 'levelname': 'INFO'}
    result = custom_fields(record_dict, {'msg': 'message', 'lvl': 'levelname'})
    assert result == {'levelname': 'INFO'}


def test_order_record_orders_and_renames():
    record_dict = {'message': 'hi', 'levelname': 'INFO'}
    result = order_record(record_dict, {'severity': 'levelname', 'msg': 'message'})
    assert list(result.keys()) == ['severity', 'msg']
    assert result == {'severity': 'INFO', 'msg': 'hi'}


def test_order_record_skips_missing_keys():
    record_dict = {'levelname': 'INFO'}
    result = order_record(record_dict, {'severity': 'levelname', 'msg': 'message'})
    assert result == {'severity': 'INFO'}


def test_custom_extra_fields_returns_non_standard_attributes():
    record = _make_record('hi')
    record.user_id = 42
    record.request_id = 'abc'
    extras = custom_extra_fields(record)
    assert extras['user_id'] == 42
    assert extras['request_id'] == 'abc'
    assert 'levelname' not in extras


def test_mutate_json_record_converts_datetime_values():
    dt = datetime(2026, 6, 13)
    result = mutate_json_record({'time': dt, 'msg': 'x', 'count': 5})
    assert result['time'] == dt.isoformat()
    assert result['msg'] == 'x'
    assert result['count'] == 5
