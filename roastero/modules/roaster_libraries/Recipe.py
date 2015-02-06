import json
from pprint import pprint

class Recipe:
    def __init__(self, file):
        # Load file into program.
        json_data = open(file)
        self.data = json.load(json_data)
        json_data.close()

        self.numRecipeSections = len(self.data["steps"])
        self.currentSection = 0

    def get_num_recipe_sections(self):
        return self.numRecipeSections

    def get_current_section(self):
        return self.currentSection

    def get_curent_fan_speed(self):
        return self.data["steps"][self.currentSection]["fanSpeed"]

    def get_current_target_temp(self):
        if(self.data["steps"][self.currentSection].get("targetTemp")):
            return self.data["steps"][self.currentSection]["targetTemp"]
        else:
            return 150

    def get_current_section_time(self):
        return self.data["steps"][self.currentSection]["sectionTime"]

    def get_current_cooling_status(self):
        if(self.data["steps"][self.currentSection].get("cooling")):
            return self.data["steps"][self.currentSection]["cooling"]
        else:
            return False
    
    def get_section_time(self, index):
        return self.data["steps"][index]["sectionTime"]

    def get_section_temp(self, index):
        if(self.data["steps"][index].get("targetTemp")):
            return self.data["steps"][index]["targetTemp"]
        else:
            return 150

    def set_next_section(self):
        self.currentSection += 1
