from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'License :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 2.7',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

setup(
    name         = 'FaBoBLE_BLE113',
    version      = '1.0.0',
    author       = 'FaBo',
    author_email = 'info@fabo.io',
    description  = "This is a library for the FaBo BLE SiliconLabs Brick.",
    url          = 'https://github.com/FaBoPlatform/FaBoBLE-BLE113-Python',
    license      = 'MIT',
    classifiers  = classifiers,
    packages     = find_packages()
)
