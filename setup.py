import sys, matplotlib
from cx_Freeze import setup, Executable

# Define openroast version
f = open('openroast/VERSION', 'r')
version = f.readline()
f.close()

# MSI shortcut folder to create the start in directory.
shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "Openroast",              # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]Openroast.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]

# Now create the table dictionary
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["openroast"]
                     "includes": ["os", "json", "matplotlib.backends.backend_qt5agg",
                        "matplotlib.animation", "serial"],
                     "excludes": ["matplotlib.backends.backend_tkagg", "tkinter"],
                     "include_files": [
                        "openroast/static",
                        "openroast/recipes",
                        "openroast/modules",
                        "openroast/VERSION",
                        "LICENSE"],
                     "icon": "openroast/static/icons/openroast-windows.ico",
                     "include_msvcr": True
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Openroast",
        version = version,
        description = "An open source cross-platform application for home coffee roasting",
        options = {"build_exe": build_exe_options, "bdist_msi": bdist_msi_options,
        "bdist_mac": {"iconfile": "openroast/static/icons/openroast-mac.icns"}},
        executables = [Executable("openroast/openroast.py",
            base=base
        )],
        data_files=matplotlib.get_py2exe_datafiles(),
	url = "http://roastero.com",
	author = "openroast",
	author_email = "admin@openroast.com",
	packages = ["openroast"]
)
