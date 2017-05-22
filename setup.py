"""A setuptools based setup module.
See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
import os
from os import path

import sys
if sys.version_info < (3,5):
    sys.exit('Sorry, Python < 3.5 is not supported')

# import version number
version = {}
with open("./openroast/version.py") as fp:
    exec(fp.read(), version)
# later on we use: version['__version__']

here = path.abspath(path.dirname(__file__))

# to include all the static files in the /static folder, recursively
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths
extra_files = package_files('openroast/static')

# Get the long description from the README file
# TODO - there's no readme.rst yet
# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()
long_description="TODO"

setup(
    name='openroast',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version['__version__'],

    description='An open source, cross-platform application for home coffee roasting',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/Roastero/Openroast',

    # Author details
    author='Roastero',
    author_email='admin@roastero.com',

    # Choose your license
    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Topic :: System :: Hardware :: Hardware Drivers',
        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='sr700 coffee roasting',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['PyQt5>=5.8,<5.9',
                      'matplotlib>=2.0,<2.1',
                      'freshroastsr700>=0.2.1'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': extra_files
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # it's more convenient for this package to create a scripts entry
    # scripts=[
    #     'bin/sr700-read-et-f'
    # ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'openroast=openroast.openroastapp:main',
        ],
    },
)
