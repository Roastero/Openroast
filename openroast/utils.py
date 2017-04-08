import os
import sys

def get_resource_filename(resname):
    """Get the absolute path to the named resource file.

    This serves widely the same purpose as pkg_resources.resource_filename(),
    but tries to avoid loading pkg_resources unless we're actually in
    an egg.
    """
    # Commented out the below, as it prevents a 'py3.5 -mpip install -e .'
    # from working properly in Linux.
    # path = os.path.dirname(os.path.abspath(__file__))
    # path = os.path.join(path,resname)
    # if os.path.exists(path):
    #     return path
    if hasattr(sys, "frozen"):
        exe_path = sys.executable
        if not isinstance(exe_path, str):
            exe_path = str(exe_path,sys.getfilesystemencoding())
        exe_dir = os.path.dirname(exe_path)
        path = os.path.join(exe_dir, resname)
        if os.path.exists(path):
            return path
    else:
        import pkg_resources
        try:
            path = pkg_resources.resource_filename("openroast",resname)
        except KeyError:
            pass
        else:
            path = os.path.abspath(path)
            if os.path.exists(path):
                return path
    raise IOError(
        "get_resource_filename - Could not locate resource '%s'" % (resname,))

def get_resource_string(resname):
    """Load the resource as bytes.

    This serves widely the same purpose as pkg_resources.resource_string(),
    but tries to avoid loading pkg_resources unless we're actually in
    an egg.
    """
    fullpath = None
    string = None
    try:
        fullpath = get_resource_filename(resname)
    except IOError as e:
        raise e
    with open(fullpath, 'rb') as fd:
        string = fd.read()
    return string

