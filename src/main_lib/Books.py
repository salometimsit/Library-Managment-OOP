import csv
import os

class Books:
    # this is a factory class
    # title, author, is_loaned, copies, genre, year
    def __init__(self, title, author, is_loaned, total_books, genre, year):
        self.__title = title
        self.__author = author
        self.__is_loaned = str(is_loaned)
        self.__total_books = total_books
        self.__genre = genre
        self.__year = int(year)

    @staticmethod
    def create_book(title, author, total_books, is_loaned, genre, year):
        """Factory method to create and return a Books instance"""
        return Books(title, author, str(is_loaned), total_books, genre, int(year))

    def get_title(self):
        return str(self.__title)

    def get_author(self):
        return str(self.__author)

    def get_year(self):
        return str(self.__year)

    def get_genre(self):
        return str(self.__genre)

    def get_total_books(self):
        return int(self.__total_books)

    def get_is_loaned(self):
        return str(self.__is_loaned)

    def available_to_loan(self):
        if str(self.__is_loaned)=="No":
            return True
        return False

    def add_to_library(self):
        """Append book details to the CSV file"""
        file_path = "./src/main_lib/Excel_Tables/books.csv"  # Adjusted to your directory
        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    self.__title, self.__author, self.__total_books,
                    self.__is_loaned, self.__genre, self.__year
                ])
            print(f"Book added to library: {self.__title}")
        except Exception as e:
            print(f"Failed to add book {self.__title}: {e}")

    def remove_from_library(self):
        """Logic for removing a book - requires implementation"""
        if self.__total_books > 0:
            self.__total_books -= 1
            if self.__is_loaned > 0:
                self.__is_loaned -= 1
        else:
            print("No copies left to remove.")

    def borrow_book(self):
        """Decrease the available copies if one is borrowed"""
        if self.__is_loaned > 0:
            self.__is_loaned -= 1
        else:
            print("No available copies to borrow.")

    def return_book(self):
        """Increase the available copies if one is returned"""
        if self.__is_loaned < self.__total_books:
            self.__is_loaned += 1
        else:
            print("All copies are already in the library.")

    def compare_books(self, book):
        if(self.get_title()== book.get_title() and self.get_author() == book.get_author()
                and self.get_year() == book.get_year() and self.get_genre() == book.get_genre()):
            return True
        return False


    def __str__(self):
        """String representation of the book"""
        return (
            f"Title: {self.__title}, Author: {self.__author}, Available Copies: {self.__is_loaned}, "
            f"Total Copies: {self.__total_books}, Genre: {self.__genre}, Year: {self.__year}"
        )


if __name__ == "__main__":
    book=Books("salome","salome","Yes",10,"salome",2002)
    book1=Books("itay","itay","No",10,"itay",1999)
    print(book.available_to_loan())
    print(book1.available_to_loan())