import json
from pprint import pprint

class Recipe:
    def __init__(self, roaster):
        self.roaster = roaster
        self.currentRecipeStep = 0

        # Tells if a recipe has been loaded
        self.recipeLoaded = False

        # Pass Recipe object to Roaster object
        self.roaster.pass_recipe_object(self)

    def load_recipe_json(self, recipeJson):
        self.recipe = recipeJson
        self.recipeLoaded = True

    def load_recipe_file(self, recipeFile):
        # Load recipe file
        recipeFileHandler = open(recipeFile)
        self.recipe = json.load(recipeFileHandler)
        recipeFileHandler.close()
        self.recipeLoaded = True

    def check_recipe_loaded(self):
        return self.recipeLoaded

    def get_num_recipe_sections(self):
        return len(self.recipe["steps"])

    def get_current_step_number(self):
        return self.currentRecipeStep

    def get_curent_fan_speed(self):
        return self.recipe["steps"][self.currentRecipeStep]["fanSpeed"]

    def get_current_target_temp(self):
        if(self.recipe["steps"][self.currentRecipeStep].get("targetTemp")):
            return self.recipe["steps"][self.currentRecipeStep]["targetTemp"]
        else:
            return 150

    def get_current_section_time(self):
        return self.recipe["steps"][self.currentRecipeStep]["sectionTime"]

    def get_current_cooling_status(self):
        if(self.recipe["steps"][self.currentRecipeStep].get("cooling")):
            return self.recipe["steps"][self.currentRecipeStep]["cooling"]
        else:
            return False

    def get_section_time(self, index):
        return self.recipe["steps"][index]["sectionTime"]

    def get_section_temp(self, index):
        if(self.recipe["steps"][index].get("targetTemp")):
            return self.recipe["steps"][index]["targetTemp"]
        else:
            return 150

    def set_roaster_settings(self, targetTemp, fanSpeed, sectionTime, cooling):
        if cooling:
            self.roaster.cooling_phase()
        else:
            self.roaster.set_target_temp(targetTemp)

        self.roaster.set_fan_speed(fanSpeed)
        self.roaster.set_section_time(sectionTime)

    def load_current_section(self):
        self.set_roaster_settings(targetTemp=self.recipe["steps"][self.currentRecipeStep]["targetTemp"],
                                fanSpeed=self.recipe["steps"][self.currentRecipeStep]["fanSpeed"],
                                sectionTime=self.recipe["steps"][self.currentRecipeStep]["sectionTime"],
                                cooling=self.get_current_cooling_status())

    def move_to_next_section(self):
        self.currentRecipeStep += 1
        if self.currentRecipeStep > get_num_recipe_sections:
            self.roaster.sleep()
        else:
            self.load_current_section()
