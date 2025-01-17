import unittest
import pandas as pd
import numpy as np

from src.main_lib.BookIterator import BookIterator


class TestBookIterator(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'title': ['Harry Potter', 'Lord of the Rings', 'The Hobbit', '1984'],
            'author': ['Rowling', 'Tolkien', 'Tolkien', 'Orwell'],
            'is_loaned':["No","Yes","No","Yes"],
            'copies':[2,5,3,5],
            'genre': ['Action', 'Drama', 'Fiction', 'Comedy'],
            'year': [1997, 1954, 1937, 1949],
            'popularity': [0,6,3,2]
        })

    def test_single_column_search(self):
        iterator = BookIterator(self.df, column='author', value='Tolkien')
        books = list(iterator)
        self.assertEqual(len(books), 2)
        self.assertTrue(all(book['author'] == 'Tolkien' for book in books))

    def test_upper_and_lower_unmatch(self):
        iterator = BookIterator(self.df, column='author', value='tOlKiEn')
        books = list(iterator)
        self.assertEqual(len(books), 2)

    def test_number_search(self):
        iterator = BookIterator(self.df, column='year', value=19)
        books = list(iterator)
        self.assertEqual(len(books), 4)

    def test_search_by_more_than_one_thing(self):
        conditions = {
            'author': 'Tolkien',
            'year': '193'
        }
        iterator = BookIterator(self.df, filter_conditions=conditions)
        books = list(iterator)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'The Hobbit')

    def test_space_sensitivity(self):
        iterator = BookIterator(self.df,column='title', value='Harry           Potter      ')
        books = list(iterator)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'Harry Potter')

    def test_empty_result(self):
        with self.assertRaises(Exception) as context:
            BookIterator(self.df, column='author', value='itay')
            self.assertIn("Search itay by author failed", str(context.exception))

    def test_part_word_search(self):
        iterator = BookIterator(self.df, column='title', value='hob')
        books = list(iterator)
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0]['title'], 'The Hobbit')

    def test_unexcited_items(self):
        df_with_nans = pd.DataFrame({
            'title': ['Book1', 'Book2', 'Book3'],
            'author': ['Author1', np.nan, 'Author3'],
            'year': [2000, 2001, np.nan]
        })
        iterator = BookIterator(df_with_nans, column='author', value='author')
        books = list(iterator)
        self.assertEqual(len(books), 2)

    def test_empty_data(self):
        empty_df = pd.DataFrame(columns=['title', 'author', 'year'])
        with self.assertRaises(Exception):
            BookIterator(empty_df, column='author', value='avshalom')

    def test_invalid_column(self):
        with self.assertRaises(KeyError):
            BookIterator(self.df, column='rating', value='4.5')


if __name__ == '__main__':
    unittest.main()