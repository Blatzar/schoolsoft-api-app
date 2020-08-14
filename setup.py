#!/usr/bin/env python3

from setuptools import setup, find_packages
import re
import io

with open('README.md', 'r') as f:
    long_description = f.read()

with io.open('anime_downloader/__version__.py', 'rt', encoding='utf8') as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

setup(
    name='schoolsoft_api',
    version=version,
    author='Blatzar',
    author_email='blatzar@gmail.com',
    description='Communicate with the official schoolsoft api',
    packages=find_packages(),
    url='https://github.com/Blatzar/schoolsoft-api-app',
    keywords=['schoolsoft', 'schedule', 'lunch', 'api'],
    install_requires=[
        'requests',
        'datetime',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
)
