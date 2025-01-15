import unittest
from unittest.mock import patch, Mock, mock_open
import pandas as pd
import io
from src.main_lib.Rentals import Rentals
from src.main_lib.Books import Books


class TestRentalsWithFiles(unittest.TestCase):

    @patch('src.main_lib.Rentals.FilesHandle')
    @patch('pandas.read_csv')
    @patch('builtins.open')
    def setUp(self, mock_open_func, mock_read_csv, mock_files_handle):
        """Setup for each test"""
        # מידע מדומה לקובץ CSV
        csv_content = "title,author,is_loaned,copies,genre,year,popularity\n" + \
                      "Test Book,Test Author,No,2,Fiction,2020,0\n"
        mock_open_func.return_value = io.StringIO(csv_content)

        # הגדרת mock עבור קריאת CSV
        mock_df = pd.DataFrame({
            'title': ['Test Book'],
            'author': ['Test Author'],
            'year': [2020],
            'genre': ['Fiction'],
            'copies': [1],
            'is_loaned': ['Yes'],
            'popularity': [0],
            'waiting_list': ['']
        })
        mock_read_csv.return_value = mock_df

        # הגדרת נתיבי הקבצים לטסטים
        self.test_files = [
            './src/Tests/Excel_Test_Tables/BookTest.csv',
            './src/Tests/Excel_Test_Tables/Available_BookTest.csv',
            './src/Tests/Excel_Test_Tables/NotAvailable_BookTest.csv'
        ]

        # הגדרת mock עבור FilesHandle
        mock_instance = mock_files_handle.return_value
        mock_instance.get_file_by_category.return_value = self.test_files

        # איפוס המופע של Rentals
        Rentals._Rentals__instance = None
        self.rentals = Rentals.get_instance()

    @patch('pandas.read_csv')
    def test_check_waiting_list(self, mock_read_csv):
        pass

    @patch('pandas.read_csv')
    def test_find_in_csv(self, mock_read_csv):
        pass

    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_add_to_waiting_list(self, mock_to_csv, mock_read_csv):
        mock_df = pd.DataFrame({
            'title': ['1984', 'A Game of Thrones'],
            'author': ['George Orwell', 'George R.R. Martin'],
            'year': [1949, 1996],
            'genre': ['Dystopian', 'Fantasy'],
            'copies': [0, 2],
            'is_loaned': ['Yes', 'No'],
            'popularity': [0, 0],
            'waiting_list': ['', '']
        })
        mock_read_csv.return_value = mock_df

        book1 = Books("1984", "George Orwell", "Yes", 5, "Dystopian", 1949, 0)
        book2 = Books("A Game of Thrones", "George R.R. Martin", "No", 2, "Fantasy", 1996, 0, )
        result1 = self.rentals.add_to_waiting_list(book1, "itay", "0548038488", "itay@segev.com")
        result2 = self.rentals.add_to_waiting_list(book2, "avi", "0539569955", "avi@segev.com")
        result3 = self.rentals.add_to_waiting_list(book1, "itay", "0547038488", "itai@segev.com")
        result4 = self.rentals.add_to_waiting_list(book1, "itay", "0548038488", "itai@segev.com")
        result5 = self.rentals.add_to_waiting_list(book1, "itay", "0547038488", "itay@segev.com")
        self.assertTrue(result1)
        self.assertFalse(result2)
        self.assertTrue(result3)
        self.assertFalse(result4)
        self.assertFalse(result5)

    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_rent_books(self, mock_to_csv, mock_read_csv):
        pass

    @patch('pandas.read_csv')
    @patch('pandas.DataFrame.to_csv')
    def test_return_books(self, mock_to_csv, mock_read_csv):
        pass


if __name__ == '__main__':
    unittest.main()