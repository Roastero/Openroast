# Standard Library Imports
import json

class Preferences:
    def __init__():
        self.defaultPreferences = {
            pidValues: {"p": 0.06, "i": 0.90, "d": 0.90},

        }
        self.additionalPreferences = {}


    def load_preferences_file(filePath=None):
        """Loads a file with user changed preferences."""
        filePath = filePath or self.preferencesFile

        with open(filePath) as json_data:
            loadedPreferences = json.load(json_data)
        return loadedPreferences

    def load_preferences(preferenceValues):
        """Change class variables according to passed variable."""



    # File to keep track of changes to preferences
    # Only add to this file if user changes value
    self.preferencesFile = os.path.expanduser('~/Documents/Roastero/preferences.json')


    # Default values

    # PID Controller Values
    PIDVALUES: {"p": 0.06, "i": 0.90, "d": 0.90}
