import os
import sys
from collections.abc import Mapping
from inspect import ismodule, getfile


class ReadOnlyDict(Mapping):

    def __init__(self, dict_):
        self._data = dict_

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)


class Settings:

    __slots__ = ('_data',)

    PYTEST_SCRIPT_NAME = 'py.test'

    def __init__(self, primary_settings, custom_settings=None, test_settings=None):
        self._data = {}
        self._load_settings(primary_settings)
        if custom_settings:
            self._load_settings(custom_settings)
        if test_settings and self._is_test_running():
            self._load_settings(test_settings)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        else:
            raise AttributeError("{} attribute doesn't exist".format(name))

    def _is_test_running(self):
        if self.PYTEST_SCRIPT_NAME == os.path.basename(sys.argv[0]):
            return True
        else:
            return False

    def _load_settings_from_file(self, file_path):
        data = {**self._data}
        if os.path.isfile(file_path):
            exec(open(file_path).read(), {}, data)
            self._data = ReadOnlyDict(data)
        else:
            raise FileNotFoundError("File {} doesn't exist".format(file_path))

    def _load_settings(self, settings):
        if ismodule(settings):
            file_path = getfile(settings)
            self._load_settings_from_file(file_path)

        elif isinstance(settings, str):
            if settings in os.environ:
                file_path = os.environ.get(settings)
            else:
                file_path = settings
            self._load_settings_from_file(file_path)

        else:
            raise TypeError('Settings must be module, file path or env variable')
