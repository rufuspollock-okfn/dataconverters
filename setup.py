from distutils.core import setup

setup(name='dataconverters',
      version='0.2',
      description='Data conversion python library and command line tool',
      author='Open Knowledge Foundation (Nigel Babu, Rufus Pollock, Dominik Moritz)',
      author_email='okfn-labs@lists.okfn.org',
      url='https://github.com/okfn/dataconverters/',
      packages=['dataconverters'],
      install_requires=[
          'messytables'
          ],
      entry_points={
            'console_scripts': [
                'dataconvert = dataconverters.cli:main'
            ]
         }
     )
