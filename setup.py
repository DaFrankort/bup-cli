from setuptools import setup, find_packages

setup(
    name = 'bup-cli',
    version = '1.0.0',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'bup = bupcli.__main__:main'
        ]
    },
    install_requires=[
        'tqdm>=4.64.0'
    ])