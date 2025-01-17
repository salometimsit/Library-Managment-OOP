import os
import unittest

from src.main_lib.FilesHandle import FilesHandle


class FilesHandleTest(unittest.TestCase):
    def setUp(self):
        try:
            test_dir = os.path.dirname(__file__)
            src_dir = os.path.dirname(test_dir)
            base_path = os.path.join(src_dir, "main_lib")

            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv', 'Excel_Tables/users.csv',
                         'Excel_Tables/logger.log']
            self.__files = []

            for filename in filenames:
                file_path = os.path.join(base_path, filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.__files.append(file_path)

            if not self.__files:
                raise ValueError("No files were successfully loaded")

        except Exception as e:
            print(f"An error occurred during setup: {e}")
            print(f"Current working directory: {os.getcwd()}")

    def test_upper_lower_case(self):
        book_files = FilesHandle().get_file_by_category("bOOk")
        user_files = FilesHandle().get_file_by_category("uSeRs.csv") #cause the start of the computer is users too
        logger = FilesHandle().get_file_by_category("LOGGeR")
        book_files2 = [self.__files[0], self.__files[1], self.__files[2]]
        self.assertEqual(book_files, book_files2)
        self.assertEqual(user_files, self.__files[3])
        self.assertEqual(logger, self.__files[4])

    def test_all_files_on_same_category(self):
        book_files = FilesHandle().get_file_by_category("bOOk")
        for file in book_files:
            self.assertTrue(os.path.exists(file) and "book" in file)


