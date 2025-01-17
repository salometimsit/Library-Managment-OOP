from unittest.mock import MagicMock

from src.Tests.TestFileManager import LibraryTestCase
from src.main_lib.Library import Library
from src.main_lib.Users import User


class ObserverTest(LibraryTestCase):
    def setUp(self):
        super().setUp()
        self.library = Library.get_instance()
        self.librarian = User("Test Librarian", "testlib", "librarian", "password123")

    def test_observer_registration(self):
        self.library.subscribe(self.librarian)
        self.assertIn(self.librarian, self.library._sub)
        self.library.unsubscribe(self.librarian)
        self.assertNotIn(self.librarian, self.library._sub)
