import pandas as pd

from src.Tests.TestFileManager import LibraryTestCase
from src.main_lib.BooksFactory import BooksFactory


class BooksFactoryTest(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.__files = [
            f"{self.test_dir}/BookTest.csv",
            f"{self.test_dir}/Available_BookTest.csv",
            f"{self.test_dir}/NotAvailable_BookTest.csv"
        ]
        self.factory = BooksFactory(self.__files)

    def check_book_exists(self, title, author, genre, year, expected_copies=None, file_path=None):
        df = pd.read_csv(file_path)
        book = df[(df['title'] == title) &(df['author'] == author) &(df['genre'] == genre) &
                  (df['year'] == year)]
        if expected_copies is not None and not book.empty:
            return not book.empty and book['copies'].iloc[0] == expected_copies
        return not book.empty

    def test_add_copies(self):
        self.factory.create_books("Test Book", "Test Author", 2, "Fiction", 2024)
        result=self.factory.create_books("Test Book", "Test Author", 5, "Fiction", 2024)
        self.assertFalse(result)
        self.assertTrue(self.check_book_exists("Test Book", "Test Author", "Fiction",
                                               2024,expected_copies=7, file_path=self.__files[0]))
        self.assertTrue(self.check_book_exists("Test Book", "Test Author", "Fiction",
                                               2024,expected_copies=7, file_path=self.__files[1]))

    def test_add_new_book(self):
        result = self.factory.create_books("New Book", "New Author", 3, "Fiction", 2024)
        self.assertTrue(result)
        self.assertTrue(self.check_book_exists("New Book", "New Author", "Fiction",2024,3,self.__files[0]))
        self.assertTrue(self.check_book_exists("New Book", "New Author", "Fiction",2024,3,self.__files[1]))
        self.assertFalse(self.check_book_exists("New Book", "New Author", "Fiction", 2024, None, self.__files[2]))

    def test_invalid_input(self):
        self.assertIsNone(self.factory.create_books("New Book", "New Author", 0, "Fiction", 2024))
        self.assertIsNone(self.factory.create_books("New Book", "New Author", 3, "Fictionary", 2024))

    def test_handle_with_waiting_list(self):
        books_df = pd.read_csv(self.__files[0])
        book = {'title': 'Waiting Book', 'author': 'Test Author', 'is_loaned': 'No', 'copies': 1, 'genre': 'Fiction',
                'year': 2024, 'popularity': 0}
        books_df = pd.concat([books_df, pd.DataFrame([book])], ignore_index=True)
        books_df.to_csv(self.__files[0], index=False)
        not_available_df = pd.read_csv(self.__files[2])
        book2 = {'title': 'Waiting Book', 'author': 'Test Author', 'is_loaned': 'Yes', 'copies': 1, 'genre': 'Fiction',
                 'year': 2024, 'popularity': 0, 'waiting_list': 'Test User:1234567890:ex@ex.com'}
        not_available_df = pd.concat([not_available_df, pd.DataFrame([book2])], ignore_index=True)
        not_available_df.to_csv(self.__files[2], index=False)
        available_df = pd.read_csv(self.__files[1])
        available_df = pd.concat([available_df, pd.DataFrame([book])], ignore_index=True)
        available_df.to_csv(self.__files[1], index=False)
        result = self.factory.create_books("Waiting Book", "Test Author", 2, "Fiction", 2024)
        self.assertFalse(result)
        updated_non_avai = pd.read_csv(self.__files[2])
        updated_book = updated_non_avai[
            (updated_non_avai['title'] == 'Waiting Book') & (updated_non_avai['author'] == 'Test Author')]
        self.assertTrue(pd.isna(updated_book['waiting_list'].iloc[0]) or updated_book['waiting_list'].iloc[0] == '')
        self.assertTrue(self.check_book_exists("Waiting Book", "Test Author", "Fiction", 2024, expected_copies=3,
                                               file_path=self.__files[0]))
        self.assertTrue(self.check_book_exists("Waiting Book", "Test Author", "Fiction", 2024, expected_copies=1,
                                               file_path=self.__files[1]))
        self.assertTrue(self.check_book_exists("Waiting Book", "Test Author", "Fiction", 2024, expected_copies=2,
                                               file_path=self.__files[2]))



