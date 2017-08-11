from setuptools import setup, find_packages

from my_settings import __version__


INSTALL_REQUIRES = ()
EXTRAS_REQUIRE = {'dev': ('pytest==3.2.0', 'pdbpp==0.9.1')}
LONG_DESCRIPTION = '''
my_settings can load your settings from python module, 
env variable and file path which has to lead to python module.
You can have three types of settings files:
1) primary(usually plays role of base settings file which is included in a project) 
2) custom(your custom settings file for certain deployment case)
3) test(your settings file for tests)

all settings files overlap each other in this sequence: test -> custom -> primary
'''



setup(
    name='my_settings',
    author='Greg Eremeev',
    author_email='gregory.eremeev@gmail.com',
    version=__version__,
    description='Convenient and simple settings for any project',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/plain',
    license='MIT',
    packages=find_packages(),
    url='https://github.com/GregEremeev/my_settings',
    zip_safe=False,
    python_requires='>=3.3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    include_package_data=True,
)
