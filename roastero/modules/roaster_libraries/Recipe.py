# Standard Library Imports
import json

class Recipe:
    def __init__(self, roaster):
        self.roaster = roaster
        self.currentRecipeStep = 0

        # Stores recipe
        self.recipe = {}

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

    def clear_recipe(self):
        self.recipeLoaded = False
        self.recipe = {}
        self.currentRecipeStep = 0

    def check_recipe_loaded(self):
        return self.recipeLoaded

    def get_num_recipe_sections(self):
        return len(self.recipe["steps"])

    def get_current_step_number(self):
        return self.currentRecipeStep

    def get_current_fan_speed(self):
        return self.recipe["steps"][self.currentRecipeStep]["fanSpeed"]

    def get_current_target_temp(self):
        if(self.recipe["steps"][self.currentRecipeStep].get("targetTemp")):
            return self.recipe["steps"][self.currentRecipeStep]["targetTemp"]
        else:
            return 150

    def get_current_section_time(self):
        return self.recipe["steps"][self.currentRecipeStep]["sectionTime"]

    def restart_current_recipe(self):
        self.currentRecipeStep = 0
        self.load_current_section()

    def more_recipe_sections(self):
        if(len(self.recipe["steps"]) - self.currentRecipeStep == 0):
            return False
        else:
            return True

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

    def reset_roaster_settings(self):
        self.set_roaster_settings(targetTemp=150, fanSpeed=1, sectionTime=0, cooling=False)

    def set_roaster_settings(self, targetTemp, fanSpeed, sectionTime, cooling):
        if cooling:
            self.roaster.cooling_phase()
        else:
            self.roaster.set_target_temp(targetTemp)

        self.roaster.set_fan_speed(fanSpeed)
        self.roaster.set_section_time(sectionTime)

    def load_current_section(self):
        self.set_roaster_settings(self.get_current_target_temp(),
                                self.get_current_fan_speed(),
                                self.get_current_section_time(),
                                self.get_current_cooling_status())

    def move_to_next_section(self):
        if (self.currentRecipeStep + 1) >= self.get_num_recipe_sections():
            self.roaster.sleep()
        else:
            self.currentRecipeStep += 1
            self.load_current_section()

    def cool_beans(self):
        # set step to last step
        self.currentRecipeStep = self.get_num_recipe_sections()

        # Have the roaster cool
        self.roaster.cooling_phase()

    def get_current_recipe(self):
        return self.recipe
