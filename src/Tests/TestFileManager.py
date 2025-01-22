import os
import shutil
import unittest
import pandas as pd
from unittest.mock import patch, Mock


class TestFileManager:
    """
    Manages test files for the library system tests
    """

    @staticmethod
    def create_test_directory():
        """
        creates the test files directory
        """
        test_dir = "test_Excel_Tables"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        os.makedirs(test_dir)
        return test_dir

    @staticmethod
    def create_test_files(test_dir):
        """
        creates all the files for the tests
        """
        # Books.csv
        books_data = {'title': ['Test Book 1', 'Test Book 2'],'author': ['Test Author 1', 'Test Author 2'],
            'is_loaned': ['No', 'Yes'],'copies': [5, 3],'genre': ['Fiction', 'Drama'],'year': [2020, 2021],
            'popularity': [0, 0]}
        pd.DataFrame(books_data).to_csv(f"{test_dir}/BookTest.csv", index=False)

        # available_books.csv
        available_data = {'title': ['Test Book 1'],'author': ['Test Author 1'],'is_loaned': ['No'],'copies': [5],
            'genre': ['Fiction'],'year': [2020],'popularity': [0]}
        pd.DataFrame(available_data).to_csv(f"{test_dir}/Available_BookTest.csv", index=False)

        # not_available_books.csv
        not_available_data = {'title': ['Test Book 2'],'author': ['Test Author 2'],'is_loaned': ['Yes'],'copies': [3],
            'genre': ['Drama'],'year': [2021],'popularity': [0],'waiting_list': ['']}
        pd.DataFrame(not_available_data).to_csv(f"{test_dir}/NotAvailable_BookTest.csv", index=False)

        # users.csv
        users_data = {'name': ['Test User'],'username': ['testuser'],'role': ['librarian'],
                      'password': ['hashedpassword']}
        pd.DataFrame(users_data).to_csv(f"{test_dir}/UsersTest.csv", index=False)

        # logger.log
        with open(f"{test_dir}/LoggerTest.log", 'w') as f:
            pass

    @staticmethod
    def cleanup_test_files():
        """
        removes the directory and all the files from the test files
        """
        test_dir = "test_Excel_Tables"
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


class LibraryTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        set up test before any tests this is a father class
        """

        cls.test_dir = TestFileManager.create_test_directory()
        TestFileManager.create_test_files(cls.test_dir)

        #using mock for replacing the new files by the older
        cls.files_handle_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_all_files')
        cls.mock_get_all_files = cls.files_handle_patcher.start()
        cls.mock_get_all_files.return_value = [f"{cls.test_dir}/BookTest.csv",f"{cls.test_dir}/Available_BookTest.csv",
            f"{cls.test_dir}/NotAvailable_BookTest.csv",f"{cls.test_dir}/UsersTest.csv",f"{cls.test_dir}/LoggerTest.log"]

        # replacing the get file by category method
        cls.category_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_file_by_category')
        cls.mock_category = cls.category_patcher.start()

        def mock_get_file_by_category(category):
            """
            replacing the real method and send those files instead
            :param category:
            :return:
            """
            if category == "book":
                return [f"{cls.test_dir}/BookTest.csv",f"{cls.test_dir}/Available_BookTest.csv",
                        f"{cls.test_dir}/NotAvailable_BookTest.csv"]
            elif category == "users.csv":
                return f"{cls.test_dir}/UsersTest.csv"
            else:
                return f"{cls.test_dir}/{category}"

        cls.mock_category.side_effect = mock_get_file_by_category

        # mock for logger
        cls.logger_patcher = patch('src.main_lib.FilesHandle.FilesHandle.get_logger_file')
        cls.mock_logger = cls.logger_patcher.start()
        cls.mock_logger.return_value = f"{cls.test_dir}/LoggerTest.log"

    @classmethod
    def tearDownClass(cls):
        """
        cleaning after all the tests
        """
        cls.files_handle_patcher.stop()
        cls.category_patcher.stop()
        cls.logger_patcher.stop()
        TestFileManager.cleanup_test_files()

    def setUp(self):
        """
        before each test it will set up all the files
        """
        TestFileManager.create_test_files(self.test_dir)