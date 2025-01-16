import unittest
import pandas as pd
from src.main_lib.SearchStrategy import *

class TestSearchStrategies(unittest.TestCase):
    """
    test class to check that all the searches works, we created a mock dataframe to see that it works
    """
    def setUp(self):
        # Sample data for testing
        self.df = pd.DataFrame({
            "title": ["War and Peace", "Great Expectations", "The Divine Comedy"],
            "author": ["Leo Tolstoy", "Charles Dickens", "Dante Alighieri"],
            "year": ["1869", "1861", "1320"],
            "genre": ["Historical Fiction", "Classic", "Epic Poetry"]
        })

    def test_title_search(self):
        search = TitleSearch()
        result = search.search(self.df, "War and Peace")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "War and Peace")

    def test_author_search(self):
        search = AuthorSearch()
        result = search.search(self.df, "Charles Dickens")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["author"], "Charles Dickens")

    def test_year_search(self):
        search = YearSearch()
        result = search.search(self.df, "1861")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["year"], "1861")

    def test_genre_search(self):
        search = GenreSearch()
        result = search.search(self.df, "Epic Poetry")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["genre"], "Epic Poetry")

if __name__ == "__main__":
    unittest.main()
