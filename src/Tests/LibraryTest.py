from TestFileManager import LibraryTestCase
from src.main_lib.Books import Books
from src.main_lib.Library import Library
from src.main_lib.Users import User
import pandas as pd


class LibraryTest(LibraryTestCase):
    def setUp(self):
        super().setUp()

        self.library = Library.get_instance()

        self.test_name = "Test"
        self.test_username = "testlib"
        self.test_password = "test123"

        self.library.user_register(fullname=self.test_name,
            username=self.test_username,password=self.test_password
        )


    def test_user_login_logout_cycle(self):
        self.assertTrue(self.library.user_login(self.test_username, self.test_password))
        self.assertTrue(self.library.check_login())

        self.assertTrue(self.library.user_logout())
        self.assertFalse(self.library.check_login())


    def test_librarian_notification_subscription(self):
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


    def test_display_genre(self):
        self.library.user_login(self.test_username, self.test_password)
        self.library.add_item(type="book", title="Fiction Book", author="Author1",copies=1, genre="Fiction", year=2024)
        self.library.add_item(type="book", title="Drama Book", author="Author2",copies=1, genre="Drama", year=2024)

        fiction_books = self.library.display_genre("Fiction")
        self.assertTrue(any(book['title'] == "Fiction Book" for book in fiction_books))
        self.assertFalse(any(book['title'] == "Drama Book" for book in fiction_books))

        empty_result = self.library.display_genre("NonExistentGenre")
        self.assertEqual(len(empty_result), 0)


    def test_waiting_list_system(self):
        self.library.user_login(self.test_username, self.test_password)
        self.library.add_item(type="book", title="Popular Book",
                              author="Author", copies=1, genre="Fiction", year=2024)
        test_book = Books("Popular Book", "Author", "No", 1, "Fiction", 2024, 0)
        self.library.rent_book(test_book)
        # Add user to waiting list
        result = self.library.add_to_waiting_list(test_book, "Waiting User", "1234567890", "test@email.com")
        self.assertTrue(result)
        # Try to add same user again
        result = self.library.add_to_waiting_list(test_book, "Waiting User", "1234567890", "test@email.com")
        self.assertFalse(result)


    def test_add_and_delete_book(self):
        """Test adding and deleting a book"""
        self.library.user_login(self.test_username, self.test_password)
        result = self.library.add_item(type="book",title="Test Book15",
            author="Test Author",copies=1,genre="Fiction",year=2024)
        test_book=Books("Test Book15","Test Author","No",1,"Fiction",2024,0)
        # Verify book was added by searching for it
        search_result = self.library.search_book("Test Book15", "title")
        self.assertTrue(len(search_result) > 0)
        self.assertTrue(result)
        delete_result = self.library.delete_book(test_book)
        self.assertTrue(delete_result)
        # Verify book was deleted
        search_result = self.library.search_book("Test Book15", 'title')
        self.assertEqual(len(search_result), 0)


    def test_book_rental_system(self):
        """Test the book rental functionality"""
        self.library.user_login(self.test_username, self.test_password)
        self.library.add_item(type="Book",title="Rental Test Book",
            author="Test Author",copies=1,
            genre="Fiction",year=2024
        )
        test_book=Books("Rental Test Book","Test Author","No",1,"Fiction",2024,0)
        rent= self.library.rent_book(test_book)
        self.assertTrue(rent)
        not_available = self.library.display_not_available_books()
        self.assertTrue(any(book['title'] == "Rental Test Book" for book in not_available))
        self.assertTrue(self.library.return_book(test_book))
        available = self.library.display_available_books()
        self.assertTrue(any(book['title'] == "Rental Test Book" for book in available))


    def test_non_good_pass_user(self):
        self.assertFalse(self.library.user_login(self.test_username, "wrong_password"))
        self.assertFalse(self.library.user_login("nonexistent_user", "password"))
        self.assertFalse(self.library.check_login())


    def test_duplicate_register(self):
        self.assertTrue(self.library.user_register("Test User", "testuser", "password123"))
        self.assertFalse(self.library.user_register("Another User", "testuser", "different_password"))


    def test_waiting_list_system(self):
        self.library.user_login(self.test_username, self.test_password)

        self.library.add_item(type="book", title="Popular Book",
                              author="Author", copies=1, genre="Fiction", year=2024)
        test_book = Books("Popular Book", "Author", "No", 1, "Fiction", 2024, 0)
        self.library.rent_book(test_book)

        result = self.library.add_to_waiting_list(test_book, "Waiting User", "1234567890", "test@email.com")
        self.assertTrue(result)

        result = self.library.add_to_waiting_list(test_book, "Waiting Users", "1234537890", "test@email.com")
        self.assertFalse(result)


    def test_display_popular_books(self):
        self.library.user_login(self.test_username, self.test_password)
        for i in range(15):
            self.library.add_item(type="book", title=f"Book{i}",
                                  author=f"Author{i}", copies=1, genre="Fiction", year=2024)
            test_book = Books(f"Book{i}", f"Author{i}", "No", 1, "Fiction", 2024, i)
            if i > 5:
                self.library.rent_book(test_book)

        popular_books = self.library.display_popular_books()

        self.assertEqual(len(popular_books), 10)

        popularity = [book['popularity'] for book in popular_books]
        self.assertEqual(popularity, sorted(popularity, reverse=True))

    def tearDown(self):
        """Clean up after tests"""
        super().tearDown()
        # Additional cleanup if needed
        self.library.user_logout()
        Library._Library__instance = None  # Reset singleton instance