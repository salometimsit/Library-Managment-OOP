import csv
import os

import pandas as pd

from src.main_lib.Books import Books
from src.main_lib.LibraryServiceLocator import LibraryServiceLocator
from src.main_lib.Logger import Logger
from src.main_lib.BooksFactory import BooksFactory
from src.main_lib.Delete_Books import DeleteBooks
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
        if Library.__instance is None:
            super().__init__()
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
            LibraryServiceLocator.set_library(self)
            from src.main_lib.Rentals import Rentals
            Rentals.get_instance()
            self.current_librarian=None


    @staticmethod
    def get_instance():
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def set_current_librarian(self, librarian):
        self.current_librarian = librarian
        self.sub=[]
        if librarian and librarian.get_role() == "librarian":
            self.subscribe(librarian)
            self.sub.append(librarian)

    def get_rentals(self):
        return LibraryServiceLocator.get_rentals()

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

    @Logger.log_method_call("Book added")
    def add_book(self, title, author, copies, genre, year):
        """
        Adds a new book to the library if it does not already exist.

        Args:
            new_book (Books): Book instance to be added.

        Returns:
            bool: True if the book was added, False otherwise.
        """
        return self.facbooks.create_books(title, author, copies, genre, year)

    @Logger.log_method_call("book removed")
    def delete_book(self, book):
        try:
            return DeleteBooks.delete_books(book)
        except Exception:
            return False

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
        new_user=User(name, username, role, password)
        if role == "librarian":
            self.subscribe(new_user)


    def rent_book(self, book):
        rentals = self.get_rentals()
        return rentals.rent_books(book)


    def return_book(self, book):
        """
        Returns a book from a client.

        Args:
            book (Books): Book to be returned.
        """
        rentals = self.get_rentals()
        return rentals.return_books(book)

    def display_all_books(self):
        df = pd.read_csv(self.__files[0])
        if df.empty:
            Logger.log_add_message("Displayed all books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed all books successfully")
        return df.to_dict(orient='records')

    def display_not_available_books(self):
        df = pd.read_csv(self.__files[2])
        if df.empty:
            Logger.log_add_message("Displayed borrowed books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed borrowed books successfully")
        return df.to_dict(orient='records')

    def display_available_books(self):
        df = pd.read_csv(self.__files[1])
        if df.empty:
            Logger.log_add_message("Displayed available books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed available books successfully")
        return df.to_dict(orient='records')

    def display_popular_books(self):
        df = pd.read_csv(self.__files[0])
        if df.empty:
            Logger.log_add_message("Displayed popular books fail")
            raise FileNotFoundError("File not found")
        if 'popularity' not in df.columns:
            Logger.log_add_message("Displayed popular books fail")
            raise KeyError("Column 'popularity' not found in the dataset")
        top_10_books = df.sort_values(by='popularity', ascending=False).head(10)
        Logger.log_add_message("Displayed popular books successfully")
        return top_10_books.to_dict(orient='records')

    def search_book(self, name, strategy):
        self.searcher.set_strategy(strategy)
        df = self.searcher.search_all(name)
        if df == []:
            Logger.log_add_message(f"Search book '{name}' by {strategy} name completed fail")
        else:
            Logger.log_add_message(f"Search book '{name}' by {strategy} name completed successfully")
        return df

    def notify(self, message):
        if hasattr(self, 'current_librarian') and self.current_librarian:
            if self.current_librarian not in self.sub:
                self.sub = []
                self.subscribe(self.current_librarian)
            self.current_librarian.update(self, message)



if __name__ == '__main__':
    books_library = Library.get_instance()
    # books_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 10, "Fiction", 1925)
    book = Books("eytan life story", "eytan nalimov", "No", 3, "Psychological Drama", 2004, 0)
    books_library.delete_book(book)
    print(books_library)
