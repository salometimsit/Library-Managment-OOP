from src.Tests.TestFileManager import LibraryTestCase
from src.main_lib.SearchStrategy import TitleSearch, AuthorSearch, YearSearch, GenreSearch
from src.main_lib.Search_Books import SearchBooks


class SearchBooksTest(LibraryTestCase):
    def setUp(self):
        super().setUp()

    def test_set_strategy(self):
        search = SearchBooks()
        search.set_strategy("title")
        self.assertIsInstance(search._SearchBooks__strategy, TitleSearch)
        search.set_strategy("author")
        self.assertIsInstance(search._SearchBooks__strategy, AuthorSearch)
        search.set_strategy("year")
        self.assertIsInstance(search._SearchBooks__strategy, YearSearch)
        search.set_strategy("genre")
        self.assertIsInstance(search._SearchBooks__strategy, GenreSearch)
        search.set_strategy("TITLE")
        self.assertIsInstance(search._SearchBooks__strategy, TitleSearch)
        with self.assertRaises(Exception):
            search.set_strategy("copies")

    def test_search_all(self):
        search = SearchBooks()
        search.set_strategy("title")
        results = search.search_all("Test Book 1")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["title"], "Test Book 1")

        results = search.search_all("bla")
        self.assertEqual(len(results), 0)

        search.set_strategy("author")
        results = search.search_all("Test Author")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["author"], "Test Author 1")

    def test_search_loaned(self):
        search = SearchBooks()
        search.set_strategy("title")
        results = search.search_loaned("Test Book 2")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["is_loaned"], "Yes")
        results = search.search_loaned("Test Book 1")
        self.assertEqual(len(results), 0)

    def test_search_available(self):
        search = SearchBooks()
        search.set_strategy("title")
        results = search.search_available("Test Book")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0]["title"], "Test Book 1")
        self.assertEqual(results[0]["is_loaned"], "No")
        search.set_strategy("author")
        results = search.search_available("Test Author")
        self.assertTrue(len(results) > 0)

    def test_not_good_search_cases(self):
        search = SearchBooks()
        search.set_strategy("title")
        with self.assertRaises(Exception):
            search.search_all("")
        results = search.search_all("Test@Book#1")
        self.assertEqual(len(results), 0)
        with self.assertRaises(Exception):
            search.search_all("   ")
        results_lower = search.search_all("test book 1")
        results_upper = search.search_all("TEST BOOK 1")
        self.assertEqual(len(results_lower), len(results_upper))
        search = SearchBooks()
        with self.assertRaises(AttributeError):
            search.search_all("Test Book 1")

    def test_search_year(self):
        search = SearchBooks()
        search.set_strategy("year")
        result=search.search_all(2020)
        self.assertTrue(len(result) == 1)
        self.assertEqual(result[0]["year"], 2020)
        result=search.search_all(202)
        self.assertTrue(len(result) == 2)
        result=search.search_all("two thousand years")
        self.assertTrue(len(result) == 0)


