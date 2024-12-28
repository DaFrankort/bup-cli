from setuptools import setup, find_packages

setup(
    name = 'bup-cli',
    version = '0.1.0',
    packages = ['bupcli'],
    entry_points = {
        'console_scripts': [
            'bup = bupcli.__main__:main'
       , ]
    })