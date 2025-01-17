from TestFileManager import LibraryTestCase
from src.main_lib.Library import Library
from src.main_lib.Users import User
import pandas as pd


class LibraryTest(LibraryTestCase):
    def setUp(self):
        """Initialize test environment"""
        super().setUp()  # This will set up any necessary test files/directories

        # Initialize library instance
        self.library = Library.get_instance()

        # Create a test librarian
        self.test_name = "Test"
        self.test_username = "testlib"
        self.test_password = "test123"

        # Register test librarian
        self.library.user_register(fullname=self.test_name,
            username=self.test_username,password=self.test_password
        )

    def test_user_login_logout_cycle(self):
        """Test the complete login/logout cycle"""
        # Test successful login
        self.assertTrue(self.library.user_login(self.test_username, self.test_password))
        self.assertTrue(self.library.check_login())

        # Test logout
        self.assertTrue(self.library.user_logout())
        self.assertFalse(self.library.check_login())

    def test_librarian_notification_subscription(self):
        """Test that librarians are properly subscribed to notifications"""
        # Login the librarian
        self.library.user_login(self.test_username, self.test_password)
        # Check if librarian is in subscribers list
        self.assertIn(self.library.current_librarian, self.library._sub)
        # Test notification (though we can't test the GUI popup directly)
        self.library.notify("Test notification")
        # Ensure librarian stays in subscribers after notification
        self.assertIn(self.library.current_librarian, self.library._sub)

    def test_singleton_pattern(self):
        """Test that Library implements singleton pattern correctly"""
        library1 = Library.get_instance()
        library2 = Library.get_instance()
        singleton = Library.get_instance()
        new_library = Library()
        self.assertIs(library1, library2)
        self.assertIs(library1, self.library)
        self.assertIsNot(singleton,new_library)
        self.assertEqual(type(singleton), type(new_library))
    def test_add_and_delete_book(self):
        """Test adding and deleting a book"""
        self.library.user_login(self.test_username, self.test_password)
        test_book = self.library.add_item(type="book",title="Test Book",
            author="Test Author",copies=1,genre="Fiction",year=2024)
        # Verify book was added by searching for it
        search_result = self.library.search_book("Test Book", "title")
        self.assertTrue(len(search_result) > 0)
        delete_result = self.library.delete_book(test_book)
        self.assertTrue(delete_result)

        # Verify book was deleted
        search_result = self.library.search_book("Test Book", "title")
        self.assertEqual(len(search_result), 0)

    def test_book_rental_system(self):
        """Test the book rental functionality"""

        self.library.user_login(self.test_username, self.test_password)
        test_book = self.library.add_item(type="Book",title="Rental Test Book",
            author="Test Author",copies=1,
            genre="Fiction",year=2024
        )
        rent= self.library.rent_book(test_book)
        print(rent)
        self.assertTrue(rent)
        not_available = self.library.display_not_available_books()
        self.assertTrue(any(book['title'] == "Rental Test Book" for book in not_available))
        self.assertTrue(self.library.return_book(test_book))
        available = self.library.display_available_books()
        self.assertTrue(any(book['title'] == "Rental Test Book" for book in available))

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()
        # Additional cleanup if needed
        self.library.user_logout()
        Library._Library__instance = None  # Reset singleton instance