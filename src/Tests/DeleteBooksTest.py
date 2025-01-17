import unittest

from src.main_lib.Books import Books
from src.main_lib.Delete_Books import DeleteBooks
from TestFileManager import LibraryTestCase
import pandas as pd

from src.main_lib.Rentals import Rentals


class DeleteBooksTest(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.rentals=Rentals.get_instance()
        self.books = pd.read_csv(f"{self.test_dir}/BookTest.csv")
        self.available_books = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        self.non_available_books = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        self.test_book = Books(title="Test Book 1", author="Test Author 1", is_loaned="No", total_books=5,
                               genre="Fiction", year=2020, popularity=0)

        self.unavailable_book = Books(title="Test Book 2", author="Test Author 2", is_loaned="Yes",
                                      total_books=3, genre="Drama", year=2021, popularity=0)
        self.similar_to_available_book = Books(title="Test Book 1", author="Test Author ", is_loaned="No",
                                               total_books=5,
                                               genre="Fiction", year=2020, popularity=0)
        self.similar_unavailable = Books(title="Test Book 2", author="Test Author 2", is_loaned="Yes",
                                         total_books=3, genre="Drama", year=2020, popularity=0)

    def test_delete_unavailable_book(self):
        with self.assertRaises(Exception):
            DeleteBooks.delete_books(self.unavailable_book)

    def test_delete_non_exist_book(self):
        with self.assertRaises(Exception):
            DeleteBooks.delete_books(self.similar_unavailable)

        with self.assertRaises(Exception):
            DeleteBooks.delete_books(self.similar_to_available_book)

    def test_delete_exist_book(self):
        result = DeleteBooks.delete_books(self.test_book)
        self.assertTrue(result)

    def test_check_if_really_deleted(self):
        DeleteBooks.delete_books(self.test_book)
        self.books = pd.read_csv(f"{self.test_dir}/BookTest.csv")
        self.available_books = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        deleted_from_book = self.books[
            (self.books['title'].str.strip().str.lower() == self.test_book.get_title().strip().lower()) &
            (self.books['author'].str.strip().str.lower() == self.test_book.get_author().strip().lower()) &
            (self.books['year'].astype(int) == int(self.test_book.get_year())) &
            (self.books['genre'].str.strip().str.lower() == self.test_book.get_genre().strip().lower())]

        deleted_from_avai = self.available_books[
            (self.available_books['title'].str.strip().str.lower() == self.test_book.get_title().strip().lower()) &
            (self.available_books['author'].str.strip().str.lower() == self.test_book.get_author().strip().lower()) &
            (self.available_books['year'].astype(int) == int(self.test_book.get_year())) &
            (self.available_books['genre'].str.strip().str.lower() == self.test_book.get_genre().strip().lower())]

        self.assertTrue(deleted_from_book.empty)
        self.assertTrue(deleted_from_avai.empty)

    def test_not_delete_rent_book(self):
        self.rentals.rent_books(self.test_book)
        self.books = pd.read_csv(f"{self.test_dir}/BookTest.csv")
        self.available_books = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        self.non_available_books = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        with self.assertRaises(Exception):
            DeleteBooks.delete_books(self.test_book)

        df_book=self.books[
            (self.books['title'].str.strip().str.lower() == self.test_book.get_title().strip().lower()) &
            (self.books['author'].str.strip().str.lower() == self.test_book.get_author().strip().lower()) &
            (self.books['year'].astype(int) == int(self.test_book.get_year())) &
            (self.books['genre'].str.strip().str.lower() == self.test_book.get_genre().strip().lower())]

        df_avai=self.available_books[
            (self.available_books['title'].str.strip().str.lower() == self.test_book.get_title().strip().lower()) &
            (self.available_books['author'].str.strip().str.lower() == self.test_book.get_author().strip().lower()) &
            (self.available_books['year'].astype(int) == int(self.test_book.get_year())) &
            (self.available_books['genre'].str.strip().str.lower() == self.test_book.get_genre().strip().lower())]

        df_non_avai=self.non_available_books[
            (self.non_available_books['title'].str.strip().str.lower() == self.test_book.get_title().strip().lower()) &
            (self.non_available_books['author'].str.strip().str.lower() == self.test_book.get_author().strip().lower()) &
            (self.non_available_books['year'].astype(int) == int(self.test_book.get_year())) &
            (self.non_available_books['genre'].str.strip().str.lower() == self.test_book.get_genre().strip().lower())]

        self.assertFalse(df_book.empty)
        self.assertFalse(df_avai.empty)
        self.assertFalse(df_non_avai.empty)

        self.assertEqual(df_avai['copies'].iloc[0],4)
        self.assertEqual(df_non_avai['copies'].iloc[0],1)

    def test_missing_file(self):
        import os
        os.remove(f"{self.test_dir}/BookTest.csv")
        with self.assertRaises(Exception):
            DeleteBooks.delete_books(self.test_book)

    def test_big_caps_sensitive(self):
        testbook=Books(title="TEST BOOk 1", author="Test AuTHor 1", is_loaned="no", total_books=5,
                               genre="FicTIOn", year=2020, popularity=0)
        result = DeleteBooks.delete_books(testbook)
        self.assertTrue(result)

    def test_extra_spaces(self):
        testbook=Books(title="Test    Book  1  ", author="Test  Author 1", is_loaned="No", total_books=5,
                               genre="Fiction", year=2020, popularity=0)
        result = DeleteBooks.delete_books(testbook)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()