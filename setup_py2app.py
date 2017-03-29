from setuptools import setup

APP = ['openroast/openroastapp.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'openroast/static/icons/openroast-mac.icns',
    'packages': [
        'openroast',
    ],
    'plist': {
        'CFBundleName': 'Openroast %VERSION%',
        'CFBundleShortVersionString':'%VERSION_MMP%', # must be in X.X.X format
        'CFBundleVersion': '%VERSION_MMP%',
        'CFBundleIdentifier':'org.openroast.openroast', #optional
        # 'NSHumanReadableCopyright': '@ Me 2013', #optional
        'CFBundleDevelopmentRegion': 'English', #optional - English is default
    }   

}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)