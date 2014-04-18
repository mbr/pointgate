#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pointgate',
    version='0.1dev',
    description='DynDNS-like API for PointDNS (to support older routers).',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='http://github.com/mbr/pointgate',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['flask', 'flask-appconfig', 'requests', 'gunicorn'],
    entry_points={
    }
)
