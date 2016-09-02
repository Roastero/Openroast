import os
import sys
import matplotlib
from setuptools import find_packages
from cx_Freeze import setup, Executable
import distutils
import opcode


# Read in long description and requirements.
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    long_description = f.read()
with open(os.path.join(here, 'requirements.txt')) as f:
    requires = f.read().splitlines()

# Setup variables to be used cross-platform.
name = 'Openroast'
version = '1.1.0'
description = 'An open source, cross-platform application for home coffee roasting'
license = 'GPLv3'
author = 'Roastero'
url = 'https://github.com/Roastero/openroast'
author_email = 'admin@roatero.com'

# Detetermine platform and define setup.
if sys.platform == 'win32':
    distutils_path = os.path.join(os.path.dirname(opcode.__file__), 'distutils')
    setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        license=license,
        author=author,
        url=url,
        author_email=author_email,
        include_package_data=True,
        options = {
            'build_exe': {
                'packages': ['openroast'],
                'includes': [
                    'matplotlib',
                    'serial',
                    'matplotlib.backends.backend_qt5agg'],
                'include_files': [
                    'static',
                    'openroast/views',
                    'openroast/controllers',
                    'LICENSE',
                    (matplotlib.get_data_path(), 'mpl-data'),
                    (distutils_path, 'distutils')],
                'excludes': ['distutils'],
                'icon': 'static/icons/openroast-windows.ico',
                'include_msvcr': True
            },
            'bdist_msi': {
                'data': {
                    'Shortcut': [(
                        'DesktopShortcut',        # Shortcut
                        'DesktopFolder',          # Directory_
                        'Openroast',              # Name
                        'TARGETDIR',              # Component_
                        '[TARGETDIR]Openroast.exe',# Target
                        None,                     # Arguments
                        None,                     # Description
                        None,                     # Hotkey
                        None,                     # Icon
                        None,                     # IconIndex
                        None,                     # ShowCmd
                        'TARGETDIR'               # WkDir
                    )]
                }
            }
        },
        executables = [
            Executable('Openroast.py', base='Win32GUI')],
        zip_safe=False,
        data_files=matplotlib.get_py2exe_datafiles(),
        packages=find_packages(),
        install_requires=requires)

elif(sys.platform == 'darwin'):
    setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        license=license,
        author=author,
        url=url,
        author_email=author_email,
        include_package_data=True,
        options = {
            'build_exe': {
                'packages': ['openroast'],
                'includes': [
                    'matplotlib',
                    'serial',
                    'distutils',
                    'matplotlib.backends.backend_qt5agg'],
                'include_files': [
                    'static',
                    'openroast/views',
                    'openroast/controllers',
                    'LICENSE',
                    (matplotlib.get_data_path(), 'mpl-data')],
                'include_msvcr': True
            },
            'bdist_mac': {'iconfile': 'static/icons/openroast-mac.icns'}},
        executables = [
            Executable('Openroast.py')],
        zip_safe=False,
        data_files=matplotlib.get_py2exe_datafiles(),
        packages=find_packages(),
        install_requires=requires)
else:
    setup(
        name=name,
        version=version,
        description=description,
        long_description=long_description,
        license=license,
        author=author,
        url=url,
        author_email=author_email,
        packages=find_packages(),
        install_requires=requires)
