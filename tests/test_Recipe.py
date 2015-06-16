import unittest
from roastero.modules.roaster_libraries.Recipe import Recipe
from roastero.modules.roaster_libraries.FreshRoastSR700 import FreshRoastSR700

class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.Roaster = FreshRoastSR700()
        self.Recipe = Recipe(self.Roaster)

    def test_creation(self):
        self.assertTrue(isinstance(self.Recipe, Recipe))
