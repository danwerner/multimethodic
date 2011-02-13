#!/usr/bin/env python
""" setup.py for multimethods-py
"""

from distutils.core import setup

setup(
    name         ='multimethods-py',
    version      = '.1',
    description  = 'clojure style multimethods for python',
    author       = 'danwerner',
    url          = 'https://github.com/danwerner/multimethods-py',
    py_modules   = ['multimethods'],
    entry_points = {},
)
