import csv
import os

import pandas as pd

from src.main_lib.BooksFactory import BooksFactory
from src.main_lib.Rentals import *
from src.main_lib.Search_Books import SearchBooks
from src.main_lib.Subject import Subject

class Library(Subject):
    """
    Represents a library system to manage books, users, and rentals.
    Implements the Singleton pattern.

    Attributes:
        __instance (Library): Singleton instance of the Library class.
        __files (list): List of file paths for books, available_books, and not_available_books CSV files.
        __books (list): List of books currently in the library.
    """

    __instance = None

    def __init__(self):
        from src.main_lib.Books import Books
        super().__init__()
        if Library.__instance is None:
            self.searcher = SearchBooks()
            # Initialize file paths
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv']
            self.__files = []
            for filename in filenames:
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.__files.append(file_path)
            self.facbooks = BooksFactory(self.__files)

            self.__books = []
            with open(self.__files[0], mode='r') as b_csv:
                reader = csv.reader(b_csv)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 6:
                        self.__books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    else:
                        print(f"Invalid row: {row}")

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the Library class.

        Returns:
            Library: Singleton instance of the Library.
        """
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def __str__(self):
        """
        Returns a string representation of all books in the library.

        Returns:
            str: String representation of the books.
        """
        return "\n".join(str(book) for book in self.__books)

    def get_books(self):
        """
        Returns the list of books in the library.

        Returns:
            list: List of Books instances.
        """
        return self.__books

    def add_book(self, title, author, copies,genre,year):
        """
        Adds a new book to the library if it does not already exist.

        Args:
            new_book (Books): Book instance to be added.

        Returns:
            bool: True if the book was added, False otherwise.
        """
        return self.facbooks.create_books(title, author, copies,genre,year)

    def add_user(self, name, username, role, password):
        """
        Adds a new user to the library system.

        Args:
            name (str): Name of the user.
            username (str): Username of the user.
            role (str): Role of the user (e.g., Librarian).
            password (str): Password for the user.
        """
        from src.main_lib.Users import User
        User(name, username, role, password)


    def add_client(self, client):
        """
        Subscribes a client to the library notifications.

        Args:
            client (Observer): Client to subscribe.
        """
        Subject.sub(self, client)

    def remove_client(self, client):
        """
        Unsubscribes a client from the library notifications.

        Args:
            client (Observer): Client to unsubscribe.
        """
        Subject.unsubscribe(self, client)

    def rent_book(self, book):
        """
        Rents a book to a client.

        Args:
            book (Books): Book to be rented.
        """
        rentals = Rentals.get_instance()
        return rentals.rent_books(book)

    def return_book(self, book):
        """
        Returns a book from a client.

        Args:
            book (Books): Book to be returned.
        """
        rentals = Rentals.get_instance()
        return rentals.return_books(book)

    def search_book(self, name,strategy):
        self.searcher.set_strategy(strategy)
        return self.searcher.search_all(name)


if __name__ == '__main__':
    books_library = Library.get_instance()
    books_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 10, "Fiction", 1925)
    print(books_library)
