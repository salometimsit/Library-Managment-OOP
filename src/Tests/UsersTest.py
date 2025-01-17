import unittest
from TestFileManager import LibraryTestCase
from src.main_lib.FilesHandle import FilesHandle
from src.main_lib.Users import User
import os
import csv


class UsersTest(LibraryTestCase):
    def setUp(self):
        super().setUp()
        # Test user data
        self.test_name = "Test"
        self.test_username = "testlib"
        self.test_role = "librarian"
        self.test_password = "test123"

        # Create a test user
        self.test_user = User(name=self.test_name,username=self.test_username,
            role=self.test_role,password=self.test_password
        )

    def test_user_creation(self):
        self.assertEqual(self.test_user.get_name(), self.test_name)
        self.assertNotEqual(self.test_user.get_name(),"becca")
        self.assertEqual(self.test_user.get_username(), self.test_username)
        self.assertNotEqual(self.test_user.get_username(), "becc")
        self.assertEqual(self.test_user.get_role(), self.test_role)
        self.assertNotEqual(self.test_user.get_role(),"student")

    def test_password_validation(self):
        """Test password validation functionality"""
        # Correct password should validate
        self.assertTrue(self.test_user.check_password(self.test_password))
        # Incorrect password should fail
        self.assertFalse(self.test_user.check_password("wrongpassword"))

    def test_user_persistence(self):
        """Test if user data is correctly saved to file"""
        # Get the path to users.csv
        file_path = FilesHandle().get_file_by_category("users.csv")

        # Check if file exists
        self.assertTrue(os.path.exists(file_path))

        # Read the file and check if user data is present
        found = False
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == self.test_username:
                    found = True
                    self.assertEqual(row['name'], self.test_name)
                    self.assertEqual(row['role'], self.test_role)
                    self.assertNotEqual(row['password'],"bla")
                    self.assertNotEqual(row['name'],"jees")
                    break

        self.assertTrue(found, "User data was not found in the CSV file")

    def test_duplicate_username(self):
        """Test that creating a user with an existing username doesn't duplicate the entry"""
        # Create first user
        first_user = User(name="First User",username=self.test_username,
            role="librarian",password="password123"
        )

        # Create second user with same username
        second_user = User(name="Second User",username=self.test_username,
            role="librarian",password="different_password"
        )

        file_path = FilesHandle().get_file_by_category("users.csv")
        username_count = 0
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == self.test_username:
                    username_count += 1

        self.assertEqual(username_count, 1, "Found duplicate username entries in the CSV file")
if __name__ == '__main__':
    unittest.main()