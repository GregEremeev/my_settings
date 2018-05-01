## my_settings

#### my_settings is a MIT licensed library written in Python 3.x which provides lightweight tool to manage your settings files

### Installation

#### Install via pip
```bash
pip install my_settings
```

#### Using in python application
```python
from my_settings.settings import Settings

import your_settings_module


settings_from_module = Settings(your_settings_module, custom_settings='/etc/your_settings.py')
settings_from_env = Settings('TEST_MODULE_PATH', custom_settings='/etc/your_settings.py', test_settings='test_settings.py')
settings_from_file_path = Settings('/etc/your_settings.py')

print(settings_from_module.SETTINGS_VARIABLE)
print(settings_from_env.SETTINGS_VARIABLE)
print(settings_from_file_path.SETTINGS_VARIABLE)
```
