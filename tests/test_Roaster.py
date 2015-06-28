import unittest
from openroast.modules.roaster_libraries.Roaster import Roaster

class TestRoaster(unittest.TestCase):
    def setUp(self):
        self.Roaster = Roaster()

    def test_creation(self):
        self.assertTrue(isinstance(self.Roaster, Roaster))
