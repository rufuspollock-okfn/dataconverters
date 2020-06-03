from setuptools import setup

setup(name='dataconverters',
      version='0.4',
      description='Data conversion python library and command line tool',
      author='Open Knowledge Foundation (Nigel Babu, Rufus Pollock, Dominik Moritz)',
      author_email='okfn-labs@lists.okfn.org',
      url='https://github.com/okfn/dataconverters/',
      packages=['dataconverters'],
      license='MIT',
      entry_points={
          'console_scripts': [
              'dataconvert = dataconverters.cli:main'
          ]
      })
