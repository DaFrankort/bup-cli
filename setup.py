from setuptools import setup, find_packages

setup(
    name = 'bup-cli',
    version = '0.1.0',
    packages = ['bup-cli'],
    entry_points = {
        'console_scripts': [
            'bup = src.__main__:main'
       , ]
    })