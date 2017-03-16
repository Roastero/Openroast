# -*- coding: utf-8 -*-
# Roastero, released under GPLv3

import json
import openroast
from multiprocessing import sharedctypes, Array
import ctypes
import freshroastsr700


class Recipe(object):
    def __init__(self, roaster, app, max_recipe_size_bytes=64*1024):
        # this object is accessed by multiple processes, in part because
        # freshroastsr700 calls Recipe.move_to_next_section() from a
        # child process.  Therefore, all data handling must be process-safe.

        # recipe step currently being applied
        self.currentRecipeStep = sharedctypes.Value('i', 0)
        # Stores recipe
        # Here, we need to use shared memory to store the recipe.
        # Tried multiprocessing.Manager, wasn't very successful with that,
        # resorting to allocating a fixed-size, large buffer to store a JSON
        # string.  This Array needs to live for the lifetime of the object.
        self.recipe_str = Array(ctypes.c_char, max_recipe_size_bytes)

        # Tells if a recipe has been loaded
        self.recipeLoaded = sharedctypes.Value('i', 0)  # boolean

        # we are not storing this object in a process-safe manner,
        # but its members are process-safe (make sure you only use
        # its process-safe members from here!)
        self.roaster=roaster
        self.app = app

    def _recipe(self):
        # retrieve the recipe as a JSON string in shared memory.
        # needed to allow freshroastsr700 to access Recipe from
        # its child process
        if self.recipeLoaded.value:
            return json.loads(self.recipe_str.value.decode('utf_8'))
        else:
            return {}

    def load_recipe_json(self, recipeJson):
        # recipeJson is actually a dict...
        self.recipe_str.value = json.dumps(recipeJson).encode('utf_8')
        self.recipeLoaded.value = 1

    def load_recipe_file(self, recipeFile):
        # Load recipe file
        recipeFileHandler = open(recipeFile)
        recipe_dict = json.load(recipeFileHandler)
        recipeFileHandler.close()
        self.load_recipe_json(recipe_dict)

    def clear_recipe(self):
        self.recipeLoaded.value = 0
        self.recipe_str.value = ''.encode('utf_8')
        self.currentRecipeStep.value = 0

    def check_recipe_loaded(self):
        return self.recipeLoaded.value != 0

    def get_num_recipe_sections(self):
        if not self.check_recipe_loaded():
            return 0
        return len(self._recipe()["steps"])

    def get_current_step_number(self):
        return self.currentRecipeStep.value

    def get_current_fan_speed(self):
        crnt_step = self.currentRecipeStep.value
        return self._recipe()["steps"][crnt_step]["fanSpeed"]

    def get_current_target_temp(self):
        crnt_step = self.currentRecipeStep.value
        if(self._recipe()["steps"][crnt_step].get("targetTemp")):
            return self._recipe()["steps"][crnt_step]["targetTemp"]
        else:
            return 150

    def get_current_section_time(self):
        crnt_step = self.currentRecipeStep.value
        return self._recipe()["steps"][crnt_step]["sectionTime"]

    def restart_current_recipe(self):
        self.currentRecipeStep.value = 0
        self.load_current_section()

    def more_recipe_sections(self):
        if not self.check_recipe_loaded():
            return False
        if(len(self._recipe()["steps"]) - self.currentRecipeStep.value == 0):
            return False
        else:
            return True

    def get_current_cooling_status(self):
        crnt_step = self.currentRecipeStep.value
        if(self._recipe()["steps"][crnt_step].get("cooling")):
            return self._recipe()["steps"][crnt_step]["cooling"]
        else:
            return False

    def get_section_time(self, index):
        return self._recipe()["steps"][index]["sectionTime"]

    def get_section_temp(self, index):
        if(self._recipe()["steps"][index].get("targetTemp")):
            return self._recipe()["steps"][index]["targetTemp"]
        else:
            return 150

    def reset_roaster_settings(self):
        self.roaster.target_temp = 150
        self.roaster.fan_speed = 1
        self.roaster.time_remaining = 0

    def set_roaster_settings(self, targetTemp, fanSpeed, sectionTime, cooling):
        if cooling:
            self.roaster.cool()

        # Prevent the roaster from starting when section time = 0 (ex clear)
        if(not cooling and sectionTime > 0 and
           self.currentRecipeStep.value > 0):
            self.roaster.roast()

        self.roaster.target_temp = targetTemp
        self.roaster.fan_speed = fanSpeed
        self.roaster.time_remaining = sectionTime

    def load_current_section(self):
        self.set_roaster_settings(self.get_current_target_temp(),
                                self.get_current_fan_speed(),
                                self.get_current_section_time(),
                                self.get_current_cooling_status())

    def move_to_next_section(self):
        # this gets called from freshroastsr700's timer process, which
        # is spawned using multiprocessing.  Therefore, all things
        # accessed in this function must be process-safe!
        if self.check_recipe_loaded():
            if(
                (self.currentRecipeStep.value + 1) >=
                    self.get_num_recipe_sections()):
                self.roaster.idle()
            else:
                self.currentRecipeStep.value += 1
                self.load_current_section()
                # call back into RoastTab window
                self.app.roasttab_flag_update_controllers()
        else:
            self.roaster.idle()

    def get_current_recipe(self):
        return self._recipe()
