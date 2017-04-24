#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='barracks_sdk',
    version='2.0.0',
    packages=['barracks_sdk'],
    author='Gregoire Weber',
    author_email='gregoire@barracks.io',
    description='Barracks SDK in Python',
    long_description=read('README.md'),
    install_requires=read('requirements.txt'),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'requests_mock', 'mock'],
    url='https://barracks.io',
    classifiers=[
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: IoT'
    ],
    license='ALv2'
)
