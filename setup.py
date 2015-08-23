#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='git-todo',
    version='0.1',
    description=
    'Tracks issues and TODOs in a standalone branch in your repository.',
    long_description=read('README.rst'),
    author='Marc Brinkmann',
    author_email='git@marcbrinkmann.de',
    url='https://github.com/mbr/git-todo',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=['click>=4.0', 'dulwich', 'arrow', 'parsley', 'visitor'],
    entry_points={
        'console_scripts': [
            'git-todo = git_todo.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ])
