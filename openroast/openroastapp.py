# -*- coding: utf-8 -*-
# Roastero, released under GPLv3
import os
import sys
import inspect
import shutil
import logging
import pathlib
import multiprocessing
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore

MOCK_HARDWARE = False
if not MOCK_HARDWARE:
    import freshroastsr700
else:
    from openroast import freshroastsr700_mock as freshroastsr700
from openroast.controllers import recipe
from openroast.views import mainwindow
from openroast import utils as utils


class OpenroastApp(object):
    """Main application class."""
    def __init__(self):
        """Set up application, styles, fonts, and global object."""
        # app
        self.app = QtWidgets.QApplication(sys.argv)
        # fonts
        # QtGui.QFontDatabase.addApplicationFont(
        #     "static/fonts/asap/asap-regular.ttf")
        qba = QtCore.QByteArray(
            utils.get_resource_string(
                "static/fonts/asap/asap-regular.ttf"
                )
            )
        QtGui.QFontDatabase.addApplicationFontFromData(qba)
        # QtGui.QFontDatabase.addApplicationFont(
        #     "static/fonts/asap/asap-bold.ttf")
        qba = QtCore.QByteArray(
            utils.get_resource_string(
                "static/fonts/asap/asap-bold.ttf"
                )
            )
        QtGui.QFontDatabase.addApplicationFontFromData(qba)
        # QtGui.QFontDatabase.addApplicationFont(
        #     "static/fonts/asap/asap-bold-italic.ttf")
        qba = QtCore.QByteArray(
            utils.get_resource_string(
                "static/fonts/asap/asap-bold-italic.ttf"
                )
            )
        QtGui.QFontDatabase.addApplicationFontFromData(qba)
        # QtGui.QFontDatabase.addApplicationFont(
        #     "static/fonts/asap/asap-italic.ttf")
        qba = QtCore.QByteArray(
            utils.get_resource_string(
                "static/fonts/asap/asap-italic.ttf"
                )
            )
        QtGui.QFontDatabase.addApplicationFontFromData(qba)
        # styles
        style = utils.get_resource_string(
            "static/mainStyle.css"
            ).decode("utf-8")
        style = style.replace(
            'static/images/downArrow.png',
            pathlib.Path(
                utils.get_resource_filename('static/images/downArrow.png')
                ).as_posix())
        style = style.replace(
            'static/images/upArrow.png',
            pathlib.Path(
                utils.get_resource_filename('static/images/upArrow.png')
                ).as_posix())
        QtWidgets.QApplication.setStyleSheet(self.app, style)

        # copy recipes to user folder, if it doesn't exist
        # (to prevent overwriting pre-existing user data!)
        self.check_user_folder()

        # initialize recipe amd roaster object
        self.roaster = freshroastsr700.freshroastsr700(thermostat=True)
        self.recipes = recipe.Recipe(self.roaster, self)
        if(not self.roaster.set_state_transition_func(
            self.recipes.move_to_next_section)):
            # signal an error somehow
            logging.error(
                "OpenroastApp.__init__ failed to set state transition "
                "callback.  This won't work."
                )

    def check_user_folder(self):
        """Checks copies user folder if no user folder exists."""
        user_folder = os.path.expanduser('~/Documents/Openroast/')

        if not os.path.isdir(user_folder):
            # shutil.copytree("static/Recipes",
            #     os.path.join(user_folder, "Recipes"))
            shutil.copytree(
                utils.get_resource_filename("static/Recipes"),
                os.path.join(user_folder, "Recipes"))

    def roasttab_flag_update_controllers(self):
        # print("app.roasttab_flag_update_controllers called")
        self.window.roast.schedule_update_controllers();

    def run(self):
        """Turn everything on."""
        self.roaster.auto_connect()
        self.window = mainwindow.MainWindow(
            self.recipes,
            self.roaster)
        self.window.show()
        sys.exit(self.app.exec_())


# def get_script_dir(follow_symlinks=True):
    # """Checks where the script is being executed from to verify the imports
    # will work properly."""
    # if getattr(sys, 'frozen', False):
        # path = os.path.abspath(sys.executable)
    # else:
        # path = inspect.getabsfile(get_script_dir)

    # if follow_symlinks:
        # path = os.path.realpath(path)

    # return os.path.dirname(path)


def main():
    #os.chdir(get_script_dir())
    os.chdir(os.path.dirname(sys.argv[0]))
    print("changing to folder %s" % os.path.dirname(sys.argv[0]))
    multiprocessing.freeze_support()
    app = OpenroastApp()
    app.run()


if __name__ == '__main__':
    main()
