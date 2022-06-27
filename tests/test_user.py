import unittest
from app.models import User

class UserModelTest(unittest.TestCase):
    
    def setUp(self):
        self.new_user = User(password = 'banana')

    def test_password_setter(self): 
        self.assertTrue(self.new_user.pass_secure is not None) #ascertains that when password is being hashed and the pass_secure has a value

    def test_no_access_password(self): #confirms our application raises an error when we try to access the password
        with self.assertRaises(AttributeError):
            self.new_user.password
    
    def test_password_verification(self):
        self.assertTrue(self.new_user.verify_password('banana'))
