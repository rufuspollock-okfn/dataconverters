#!/usr/bin/env python

from distutils.core import setup

setup(name='dataconverters',
      version='1.0',
      description='Data Conversion tools for Python',
      author='Nigel Babu',
      author_email='nigel.babu@okfn.org',
      url='https://github.com/okfn/data-converters/',
      packages=['dataconverters'],
      entry_points={
            'console_scripts': [
                'dataconvert = dataconverters.cli:main'
            ]
         }
     )
