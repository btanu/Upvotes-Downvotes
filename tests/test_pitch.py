import unittest
from app.models import Pitch

class TestPitch(unittest.TestCase):
    def setUp(self):
        self.new_pitch = Pitch(title="Lyons", content="Moringa Student")
    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))