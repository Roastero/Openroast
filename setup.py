# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read().splitlines()

setup(
    name='Openroast',
    version='1.0.0',
    description=
        'An open source, cross-platform application for home coffee roasting',
    long_description=README,
    license='GPLv3',
    author='Roastero',
    url='http://roastero.com',
    author_email='admin@roatero.com',
    packages=find_packages(),
    install_requires=requires)
