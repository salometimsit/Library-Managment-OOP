import unittest
import pandas as pd

from src.main_lib.Books import Books


class BookTest(unittest.TestCase):
    def setUp(self):
        self.book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925, 0)
        self.book2 = Books("salome", "salome", "Yes", 10, "Drama", 2002, 0)
        self.book3 = Books("itay", "itay", "No", 10, "Drama", 1999, 0)

    def test_create_new_book_with_not_exist_genre(self):
        result1 = Books.create_book("itay", "itay", "No", 10, "Dramatic", 1999, 0)
        result2 = Books.create_book("itay", "itay", "No", 10, "Drama", 1999, 0)
        self.assertFalse(Books.create_book("Title", "Author", "No", 5, "", 2000, 0))
        self.assertFalse(Books.create_book("Title", "Author", "No", 5, None, 2000, 0))
        self.assertFalse(result1)
        self.assertTrue(result2)


def test_create_dict_fromBook(self):
    dict1 = {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "is_loaned": "No", "copies": 10,
             "genre": "Fiction", "year": 1925, "popularity": 0}
    self.assertEqual(dict1, self.book1.to_dict(), "The book should be created"
                     )


def test_compare(self):
    b1 = Books("The Great Gasby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925, 0)
    b2 = Books("The Great Gatsby", "F. ScottFitzgerald", "No", 10, "Fiction", 1925, 0)
    b3 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "comedy", 1925, 0)
    b4 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1922, 0)
    b5 = Books("The Great Gatsby", "F. Scott Fitzgerald", "Yes", 10, "Fiction", 1925, 0)
    b6 = Books("The Great Gatsby", "F. Scott Fitzgerald", "Yes", 5, "Fiction", 1925, 0)
    b7 = Books("The Great Gatsby", "F. Scott Fitzgerald", "Yes", 5, "Fiction", 1925, 6)

    self.assertFalse(self.book1.compare_books(b1))
    self.assertFalse(self.book1.compare_books(b2))
    self.assertFalse(self.book1.compare_books(b3))
    self.assertFalse(self.book1.compare_books(b4))
    self.assertTrue(self.book1.compare_books(b5))
    self.assertTrue(self.book1.compare_books(b6))
    self.assertTrue(self.book1.compare_books(b7))


def test_available_to_loan(self):
    self.assertTrue(self.book1.available_to_loan())
    self.assertFalse(self.book2.available_to_loan())


def test_str(self):
    expected_str = ("Title: The Great Gatsby, Author: F. Scott Fitzgerald, Available Copies: No, "
                    "Total Copies: 10, Genre: Fiction, Year: 1925, Popularity: 0")
    self.assertEqual(str(self.book1), expected_str)


def test_edge_cases(self):
    with self.assertRaises(ValueError):
        book_1 = Books("Book", "Author", "No", 0, "Drama", 2000, 0)
    with self.assertRaises(ValueError):
        book_2 = Books("Book", "Author", "No", 1, "Drama", 2000, -1)


if __name__ == '__main__':
    unittest.main()
