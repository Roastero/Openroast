# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import sys
import shutil
import inspect


def get_script_dir(follow_symlinks=True):
    """Checks where the script is being executed from to verify the imports
    will work properly."""
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir + '/lib')

    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


os.chdir(get_script_dir())

import openroast


app = openroast.Openroast()
app.run()
