from django.apps import apps

from acronyme.apps import AcronymeAppConfig


def test_app_config_name():
    assert AcronymeAppConfig.name == 'acronyme'


def test_app_config_default_auto_field():
    assert AcronymeAppConfig.default_auto_field == 'django.db.models.BigAutoField'


def test_acronyme_is_installed():
    assert apps.is_installed('acronyme')
