import unittest
from app.models import Comments
class TestComment(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comments(id=1, comment='awesome', pitch_id=1, user_id=1)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comments))