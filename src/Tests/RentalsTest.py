import unittest
from src.main_lib.Books import Books
from src.main_lib.Rentals import Rentals
from TestFileManager import LibraryTestCase
import pandas as pd


class TestRentals(LibraryTestCase):
    def setUp(self):
        super().setUp()
        Rentals._Rentals__instance = None
        self.rentals = Rentals()
        self.test_book = Books(title="Test Book 1", author="Test Author 1", is_loaned="No", total_books=5,
                               genre="Fiction", year=2020, popularity=0 )

        self.unavailable_book = Books( title="Test Book 2", author="Test Author 2", is_loaned="Yes",
                                       total_books=3,genre="Drama",year=2021,popularity=0)

    def test_rent_available_book(self):
        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        initial_copies = df_available.loc[
            (df_available['title'] == 'Test Book 1'), 'copies'
        ].iloc[0]
        self.assertEqual(initial_copies, 5)
        result = self.rentals.rent_books(self.test_book)
        self.assertTrue(result)

        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        new_copies = df_available.loc[
            (df_available['title'] == 'Test Book 1'), 'copies'
        ].iloc[0]
        self.assertEqual(new_copies, 4)

        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        book_entry = df_not_available[
            (df_not_available['title'] == 'Test Book 1') &
            (df_not_available['author'] == 'Test Author 1')
            ]
        self.assertFalse(book_entry.empty)
        self.assertEqual(book_entry['copies'].iloc[0], 1)

    def test_rent_last_copy(self):
        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        df_available.loc[df_available['title'] == 'Test Book 1', 'copies'] = 1
        df_available.to_csv(f"{self.test_dir}/Available_BookTest.csv", index=False)

        result = self.rentals.rent_books(self.test_book)
        self.assertTrue(result)

        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        book_in_available = df_available[
            (df_available['title'] == 'Test Book 1') &
            (df_available['author'] == 'Test Author 1')
            ]
        self.assertTrue(book_in_available.empty)

        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        book_in_not_available = df_not_available[
            (df_not_available['title'] == 'Test Book 1') &
            (df_not_available['author'] == 'Test Author 1')
            ]
        self.assertFalse(book_in_not_available.empty)
        self.assertEqual(book_in_not_available['is_loaned'].iloc[0], 'Yes')

    def test_return_book(self):
        self.rentals.rent_books(self.test_book)

        result = self.rentals.return_books(self.test_book)
        self.assertTrue(result)

        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        book_in_available = df_available[
            (df_available['title'] == 'Test Book 1') &
            (df_available['author'] == 'Test Author 1')
            ]
        self.assertFalse(book_in_available.empty)
        self.assertEqual(book_in_available['copies'].iloc[0], 4)

    def test_add_to_waiting_list(self):
        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        new_book = {'title': 'Test Book 1','author': 'Test Author 1','is_loaned': 'Yes','copies': 1,'genre': 'Fiction',
            'year': 2020,'popularity': 0,'waiting_list': ''}
        df_not_available = pd.concat([df_not_available, pd.DataFrame([new_book])], ignore_index=True)
        df_not_available.to_csv(f"{self.test_dir}/NotAvailable_BookTest.csv", index=False)

        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        df_available = df_available[~((df_available['title'] == 'Test Book 1') &
                                      (df_available['author'] == 'Test Author 1'))]
        df_available.to_csv(f"{self.test_dir}/Available_BookTest.csv", index=False)

        result = self.rentals.add_to_waiting_list(self.test_book, name="Test User", phone="1234567890",
            email="test@test.com")
        self.assertTrue(result)

        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        book_entry = df_not_available[
            (df_not_available['title'] == 'Test Book 1') &
            (df_not_available['author'] == 'Test Author 1')
            ]
        self.assertIn("Test User:1234567890:test@test.com",
                      book_entry['waiting_list'].iloc[0])

    def test_add_to_waiting_list_when_available(self):
        result = self.rentals.add_to_waiting_list(
            self.test_book,
            name="Test User",
            phone="1234567890",
            email="test@test.com"
        )
        self.assertFalse(result)

    def test_check_waiting_list(self):
        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        new_book = {'title': 'Test Book 1', 'author': 'Test Author 1', 'is_loaned': 'Yes', 'copies': 1,
                    'genre': 'Fiction','year': 2020,'popularity': 0,'waiting_list': 'Test User:1234567890:test@test.com' }
        df_not_available = pd.concat([df_not_available, pd.DataFrame([new_book])], ignore_index=True)
        df_not_available.to_csv(f"{self.test_dir}/NotAvailable_BookTest.csv", index=False)

        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")
        df_available = df_available[~((df_available['title'] == 'Test Book 1') &
                                    (df_available['author'] == 'Test Author 1'))]
        df_available.to_csv(f"{self.test_dir}/Available_BookTest.csv", index=False)

        name, phone, email = self.rentals.check_waiting_list(self.test_book)
        self.assertEqual(name, "Test User")
        self.assertEqual(phone, "1234567890")
        self.assertEqual(email, "test@test.com")

        df_not_available = pd.read_csv(f"{self.test_dir}/NotAvailable_BookTest.csv")
        book_entry = df_not_available[
            (df_not_available['title'] == 'Test Book 1') &
            (df_not_available['author'] == 'Test Author 1')
        ]
        waiting_list=book_entry['waiting_list'].iloc[0]
        self.assertTrue(pd.isna(waiting_list) or waiting_list == '')

    def test_add_popularity(self):
        initial_popularity = 0
        self.rentals.add_popularity(self.test_book)

        df_books = pd.read_csv(f"{self.test_dir}/BookTest.csv")
        df_available = pd.read_csv(f"{self.test_dir}/Available_BookTest.csv")

        book_in_books = df_books[
            (df_books['title'] == 'Test Book 1') &
            (df_books['author'] == 'Test Author 1')
            ]
        book_in_available = df_available[
            (df_available['title'] == 'Test Book 1') &
            (df_available['author'] == 'Test Author 1')
            ]

        self.assertEqual(book_in_books['popularity'].iloc[0], initial_popularity + 1)
        self.assertEqual(book_in_available['popularity'].iloc[0], initial_popularity + 1)


if __name__ == '__main__':
    unittest.main()