# Standard Library Imports
import os
from configparser import ConfigParser

class Config:
    def __init__(self):
        # Declare config object
        self.config = ConfigParser()

        # Read in ini files
        self.config.read(["default_config.ini", os.path.expanduser('~/Documents/Roastero/config.ini')])

        # Place software version into config object
        f = open('VERSION', 'r')
        version = f.readline()
        f.close()
        self.config['APP'] = {'version': version}

    def get_version(self, config = None):
        config = config or self.config
        return config['APP']['version']

    def get_screenshot_directory(self, config = None):
        config = config or self.config
        return config.get("GeneralSettings", "ScreenshotDirectory", fallback = os.path.expanduser('~/Documents/Roastero/Screenshots'))

    def set_screenshot_directory(self, directory, config = None):
        config = config or self.config
        config['GeneralSettings']['ScreenshotDirectory'] = directory
        self.write_user_config()

    def get_temperature_units(self, config = None):
        config = config or self.config
        return config.get("GeneralSettings", "Units", fallback = "F")

    def set_temperature_units(self, units, config = None):
        config = config or self.config
        config['GeneralSettings']['Units'] = units
        self.write_user_config()

    def get_pid_values(self):
        PID = {p: self.get_p_value(),
                i: self.get_i_value(),
                d: self.get_d_value()}
        return PID

    def set_pid_values(self, PID, config = None):
        self.set_p_value(p = PID["P"])
        self.set_i_value(p = PID["I"])
        self.set_d_value(p = PID["D"])

    def get_p_value(self, config = None):
        config = config or self.config
        return float(config.get("PID", "P", fallback = "4.000"))

    def set_p_value(self, p, config = None):
        config = config or self.config
        config['PID']['P'] = p
        self.write_user_config()

    def get_i_value(self, config = None):
        config = config or self.config
        return float(config.get("PID", "I", fallback = "0.045"))

    def set_i_value(self, i, config = None):
        config = config or self.config
        config['PID']['I'] = i
        self.write_user_config()

    def get_d_value(self, config = None):
        config = config or self.config
        return float(config.get("PID", "D", fallback = "2.200"))

    def set_d_value(self, d, config = None):
        config = config or self.config
        config['PID']['D'] = d
        self.write_user_config()

    def get_roaster(self, config = None):
        config = config or self.config
        return config.get("Roaster", "RoasterModel", fallback = "FreshRoastSR700")

    def set_roaster(self, roaster, config = None):
        config = config or self.config
        config['Roaster']['RoasterModel'] = roaster
        self.write_user_config()

    def write_user_config(self, config = None):
        config = config or self.config
        with open(os.path.expanduser('~/Documents/Roastero/config.ini'), 'w') as configfile:
            config.write(configfile)
