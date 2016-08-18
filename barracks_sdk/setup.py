#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import barracks_sdk

setup(
    name='barracks_sdk',
    version=barracks_sdk.__version__,
    packages=find_packages(),
    author="Pierre-Olivier Dybman",
    author_email="pod+sdk@barracks.io",
    description="API implementation for Barracks",
    long_description=open('README.md').read(),
    include_package_data=True,
    install_requires=open('requirements.txt').read(),
    url='http://barracks.io',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Home Automation",
    ],
    entry_points=None,
    license="ALv2"
)

