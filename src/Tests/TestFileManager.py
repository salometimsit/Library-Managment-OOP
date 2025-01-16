import os
import shutil
import unittest
import pandas as pd
from unittest.mock import patch, Mock


class TestFileManager:
    """Manages test files for the library system tests"""

    @staticmethod
    def create_test_directory():
        """Creates test directory structure"""
        test_dir = "test_Excel_Tables"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        os.makedirs(test_dir)
        return test_dir

    @staticmethod
    def create_test_files(test_dir):
        """Creates all necessary test CSV files"""
        # Books CSV
        books_data = {
            'title': ['Test Book 1', 'Test Book 2'],
            'author': ['Test Author 1', 'Test Author 2'],
            'is_loaned': ['No', 'Yes'],
            'copies': [5, 3],
            'genre': ['Fiction', 'Drama'],
            'year': [2020, 2021],
            'popularity': [0, 0]
        }
        pd.DataFrame(books_data).to_csv(f"{test_dir}/BookTest.csv", index=False)

        # Available Books CSV
        available_data = {
            'title': ['Test Book 1'],
            'author': ['Test Author 1'],
            'is_loaned': ['No'],
            'copies': [5],
            'genre': ['Fiction'],
            'year': [2020],
            'popularity': [0]
        }
        pd.DataFrame(available_data).to_csv(f"{test_dir}/Available_BookTest.csv", index=False)

        # Not Available Books CSV
        not_available_data = {
            'title': ['Test Book 2'],
            'author': ['Test Author 2'],
            'is_loaned': ['Yes'],
            'copies': [3],
            'genre': ['Drama'],
            'year': [2021],
            'popularity': [0],
            'waiting_list': ['']
        }
        pd.DataFrame(not_available_data).to_csv(f"{test_dir}/NotAvailable_BookTest.csv", index=False)

        # Users CSV
        users_data = {
            'name': ['Test User'],
            'username': ['testuser'],
            'role': ['librarian'],
            'password': ['hashedpassword']
        }
        pd.DataFrame(users_data).to_csv(f"{test_dir}/UsersTest.csv", index=False)

        # Logger file
        with open(f"{test_dir}/LoggerTest.log", 'w') as f:
            pass

    @staticmethod
    def cleanup_test_files():
        """Removes test directory and all test files"""
        test_dir = "test_Excel_Tables"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


class LibraryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment before any tests"""
        # Create test directory and files
        cls.test_dir = TestFileManager.create_test_directory()
        TestFileManager.create_test_files(cls.test_dir)

        # Create mock for FilesHandle
        cls.files_handle_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_all_files')
        cls.mock_get_all_files = cls.files_handle_patcher.start()
        cls.mock_get_all_files.return_value = [
            f"{cls.test_dir}/BookTest.csv",
            f"{cls.test_dir}/Available_BookTest.csv",
            f"{cls.test_dir}/NotAvailable_BookTest.csv",
            f"{cls.test_dir}/UsersTest.csv",
            f"{cls.test_dir}/LoggerTest.log"
        ]

        # Create mock for get_file_by_category
        cls.category_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_file_by_category')
        cls.mock_category = cls.category_patcher.start()

        def mock_get_file_by_category(category):
            if category == "book":
                return [
                    f"{cls.test_dir}/BookTest.csv",
                    f"{cls.test_dir}/Available_BookTest.csv",
                    f"{cls.test_dir}/NotAvailable_BookTest.csv"
                ]
            elif category == "users.csv":
                return f"{cls.test_dir}/UsersTest.csv"
            else:
                return f"{cls.test_dir}/{category}"

        cls.mock_category.side_effect = mock_get_file_by_category

        # Create mock for get_logger_file
        cls.logger_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_logger_file')
        cls.mock_logger = cls.logger_patcher.start()
        cls.mock_logger.return_value = f"{cls.test_dir}/LoggerTest.log"

    @classmethod
    def tearDownClass(cls):
        """Clean up test environment after all tests"""
        cls.files_handle_patcher.stop()
        cls.category_patcher.stop()
        cls.logger_patcher.stop()
        TestFileManager.cleanup_test_files()

    def setUp(self):
        """Reset test files before each test"""
        TestFileManager.create_test_files(self.test_dir)