# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import os
import re
import shutil
import string

from serial.tools import list_ports


def check_for_user_folder():
    """ Verify that a user folder exists and create one if it does not before
    launching the application """
    openroastUserFolder = os.path.expanduser('~/Documents/openroast/')
    if not os.path.isdir(openroastUserFolder):
        shutil.copytree("recipes", os.path.join(openroastUserFolder, "recipes"))
        shutil.copyfile("config.ini", os.path.join(openroastUserFolder, "config.ini"))


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores."""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


def vid_pid_to_serial_url(vidpid):
    #Get all com ports currently connected to the system
    currentComPorts = list(list_ports.comports())
    for port in currentComPorts:
        if re.search(vidpid, port[2], flags=re.IGNORECASE):
            return port[0]
    raise LookupError('VID:PID Not found on system')
