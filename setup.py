#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = '1.1.0'

REQUIREMENTS = [
    "requests >= 1.0.0"
]

with open("readme.rst", 'r') as f:
    long_description = f.read()

setup(
    name="puush.py",
    version=VERSION,
    author="Samuel Messner",
    author_email="powpowd@gmail.com",
    url="https://github.com/obskyr/puush.py",
    download_url="https://github.com/obskyr/puush.py/tarball/v" + VERSION,
    description="A Python module for the Puush (http://puush.me/) API.",
    long_description=long_description,
    license="MIT",
    keywords="puush upload filehost rest",
    packages=['puush'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    install_requires=REQUIREMENTS
)
