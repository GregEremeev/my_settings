import os
import sys
from inspect import getfile
from importlib.util import spec_from_file_location, module_from_spec

import pytest

from my_settings.settings import Settings


class TestSettings:

    PRIMARY_SETTINGS_VALUE = {'1': 4}
    CUSTOM_SETTINGS_VALUE = (1, 2, 3)
    TEST_SETTINGS_VALUE = {5, 6, 7}
    ENV_SETTINGS = 'TEST_MODULE_PATH'
    PRIMARY_MODULE_DATA = 'TEST_SETTING = {}'.format(PRIMARY_SETTINGS_VALUE)
    CUSTOM_MODULE_DATA = 'TEST_SETTING = {}'.format(CUSTOM_SETTINGS_VALUE)
    TEST_MODULE_DATA = 'TEST_SETTING = {}'.format(TEST_SETTINGS_VALUE)

    def create_module_with_data(self, tmpdir, name, data):
        test_module_file = tmpdir.join(name)
        test_module_file.write(data)
        name, ext = os.path.splitext(name)
        test_module_spec = spec_from_file_location(name, test_module_file.strpath)
        test_module = module_from_spec(test_module_spec)
        return test_module

    def test_load_primary_settings_as_module(self, tmpdir):
        test_module = self.create_module_with_data(tmpdir, 'test_module.py',
                                                   self.PRIMARY_MODULE_DATA)
        settings = Settings(test_module)

        assert settings.TEST_SETTING == self.PRIMARY_SETTINGS_VALUE

    def test_load_primary_settings_as_env_var(self, tmpdir):
        test_module = self.create_module_with_data(tmpdir, 'test_module.py',
                                                   self.PRIMARY_MODULE_DATA)
        os.environ[self.ENV_SETTINGS] = getfile(test_module)
        settings = Settings(self.ENV_SETTINGS)

        assert settings.TEST_SETTING == self.PRIMARY_SETTINGS_VALUE

    def test_load_primary_settings_as_file_path(self, tmpdir):
        test_module = self.create_module_with_data(tmpdir, 'test_module.py',
                                                   self.PRIMARY_MODULE_DATA)
        settings = Settings(getfile(test_module))

        assert settings.TEST_SETTING == self.PRIMARY_SETTINGS_VALUE

    def test_load_custom_settings(self, tmpdir):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)
        custom_settings = self.create_module_with_data(tmpdir, 'custom_module.py',
                                                       self.CUSTOM_MODULE_DATA)
        settings = Settings(primary_settings, custom_settings)

        assert settings.TEST_SETTING == self.CUSTOM_SETTINGS_VALUE

    def test_load_test_settings(self, tmpdir):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)
        custom_settings = self.create_module_with_data(tmpdir, 'custom_module.py',
                                                       self.CUSTOM_MODULE_DATA)
        test_settings = self.create_module_with_data(tmpdir, 'test_module.py',
                                                     self.TEST_MODULE_DATA)
        settings = Settings(primary_settings, custom_settings, test_settings)

        assert settings.TEST_SETTING == self.TEST_SETTINGS_VALUE

    def test_load_test_setting_without_custom_settings(self, tmpdir):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)
        test_settings = self.create_module_with_data(tmpdir, 'test_module.py',
                                                     self.TEST_MODULE_DATA)
        settings = Settings(primary_settings, test_settings=test_settings)

        assert settings.TEST_SETTING == self.TEST_SETTINGS_VALUE

    def test_dont_load_test_settings(self, tmpdir, monkeypatch):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)
        test_settings = self.create_module_with_data(tmpdir, 'test_module.py',
                                                     self.TEST_MODULE_DATA)

        monkeypatch.setattr(sys, 'argv', [''])
        settings = Settings(primary_settings, test_settings=test_settings)

        assert settings.TEST_SETTING == self.PRIMARY_SETTINGS_VALUE

    def test_cant_change_settings(self, tmpdir):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)

        settings = Settings(primary_settings)
        with pytest.raises(AttributeError):
            settings.TEST_SETTING = 1

    def test_lazy_import(self, tmpdir):
        primary_settings = self.create_module_with_data(tmpdir, 'primary_module.py',
                                                        self.PRIMARY_MODULE_DATA)
        settings = Settings(primary_settings)
        assert settings._data == {}
        assert settings.TEST_SETTING == self.PRIMARY_SETTINGS_VALUE
