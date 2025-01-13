import csv
import os

from src.main_lib.BooksCategory import BooksCategory

class Books:
    """
    Represents a book in the library system.

    Attributes:
        __title (str): The title of the book.
        __author (str): The author of the book.
        __is_loaned (str): Indicates if the book is loaned ('Yes' or 'No').
        __total_books (int): Total number of copies available in the library.
        __genre (str): The genre of the book, validated against BooksCategory.
        __year (int): The year the book was published.
        __popularity (int): Popularity metric of the book.
    """

    def __init__(self, title, author, is_loaned, total_books, genre, year, popularity):
        """
        Initializes a Books instance.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            is_loaned (str): Loan status ('Yes' or 'No').
            total_books (int): Total copies available.
            genre (str): Genre of the book.
            year (int): Year of publication.
            popularity (int): Popularity of the book.
        """
        self.__title = title
        self.__author = author
        self.__is_loaned = str(is_loaned)
        self.__total_books = int(total_books)
        self.__genre = genre
        self.__year = int(year)
        self.__popularity = popularity

    @staticmethod
    def create_book(title, author, is_loaned, total_books, genre, year, popularity):
        """
        Factory method to create and return a Books instance.

        Args:
            title (str): Title of the book.
            author (str): Author of the book.
            total_books (int): Total copies available.
            is_loaned (str): Loan status ('Yes' or 'No').
            genre (str): Genre of the book.
            year (int): Year of publication.
            popularity (int): Popularity of the book.

        Returns:
            Books: An instance of Books if genre is valid, else None.
        """
        if genre not in BooksCategory._value2member_map_:
            print("Genre is not a valid genre")
            return None
        return Books(title, author, str(is_loaned), total_books, genre, int(year), int(popularity))

    def get_title(self):
        """Returns the title of the book."""
        return str(self.__title)

    def get_author(self):
        """Returns the author of the book."""
        return str(self.__author)

    def get_year(self):
        """Returns the year of publication."""
        return str(self.__year)

    def get_genre(self):
        """Returns the genre of the book."""
        return str(self.__genre)

    def get_total_books(self):
        """Returns the total number of copies available."""
        return int(self.__total_books)

    def get_is_loaned(self):
        """Returns the loan status of the book."""
        return str(self.__is_loaned)

    def get_popularity(self):
        """Returns the popularity of the book."""
        return int(self.__popularity)

    def set_popularity(self, popularity):
        """Sets the popularity of the book."""
        self.__popularity = popularity

    def available_to_loan(self):
        """Checks if the book is available to loan."""
        return str(self.__is_loaned) == "No"

    def to_dict(self):
        return {
            "title": self.__title,
            "author": self.__author,
            "is_loaned": self.__is_loaned,
            "copies": self.__total_books,
            "genre": self.__genre,
            "year": self.__year,
            "popularity": self.__popularity,
        }

    def compare_books(self, book):
        """
        Compares the current book with another book.

        Args:
            book (Books): The book to compare with.

        Returns:
            bool: True if the books are identical, False otherwise.
        """
        return (
            self.get_title() == book.get_title() and
            self.get_author() == book.get_author() and
            self.get_year() == book.get_year() and
            self.get_genre() == book.get_genre()
        )

    def __str__(self):
        """Returns a string representation of the book."""
        return (
            f"Title: {self.__title}, Author: {self.__author}, Available Copies: {self.__is_loaned}, "
            f"Total Copies: {self.__total_books}, Genre: {self.__genre}, Year: {self.__year}, Popularity: {self.__popularity}"
        )

if __name__ == "__main__":
    from Library import Library
    lib = Library.get_instance()
    lib.add_book("salome", "salome", 5, 10, "Drama", 2002, 0)
    lib.add_book("itay", "itay", "No", 10, "Drama", 1999, 0)
    lib.rent_book()

    book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925, 0)
