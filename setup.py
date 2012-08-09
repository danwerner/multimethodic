#!/usr/bin/env python
""" setup.py for multimethods
"""

from distutils.core import setup

setup(
    name         = 'multimethods',
    version      = '1.0',
    description  = 'Clojure-style multimethods for Python',
    author       = 'Daniel Werner',
    author_email = 'daniel.d.werner@googlemail.com',
    license      = 'BSD 2-clause',
    keywords     = 'multimethods dispatch',
    classifiers  = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    url          = 'http://github.com/danwerner/multimethods',
    py_modules   = ['multimethods'],

    long_description = "This module adds multimethod support to the Python programming language. In \
contrast to other multiple dispatch implementations, this one doesn't strictly \
dispatch on argument types, but on a user-provided dispatch function that can \
differ for each multimethod. This design is inspired the Clojure programming \
language's multimethods.",
)
