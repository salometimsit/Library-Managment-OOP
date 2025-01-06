import csv
import os

import pandas as pd

from src.main_lib.Books import Books
from src.main_lib.Rentals import *
from src.main_lib.Search_Books import SearchBooks
from src.main_lib.Subject import Subject


class Library(Subject):
    __instance = None

    def __init__(self):
        from src.main_lib.Books import Books
        super().__init__()
        if Library.__instance is None:
            # Path to books.csv inside Excel_Tables under main_lib
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv']
            self.__files = []
            for filename in filenames:
                # Path to the file inside Excel_Tables under main_lib
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.__files.append(file_path)

            self.__books = []
            with open(self.__files[0], mode='r') as b_csv:
                reader = csv.reader(b_csv)
                next(reader, None)
                for row in reader:
                    if len(row) >= 6:
                        self.__books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    else:
                        print(f"Invalid row: {row}")

    @staticmethod
    def get_instance():
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def __str__(self):
        s = ""
        for book in self.__books:
            s += str(book) + "\n"
        return s

    def get_books(self):
        return self.__books

    def add_book(self, title, author, available_copies, total_books, genre, year, popularity):
        flag = True
        new_book = Books.create_book(title, author, available_copies, total_books, genre, year, popularity)
        if new_book is None:
            return False
        for book in self.__books:
            if new_book.compare_books(book):
                flag = False
        if flag:
            self.__books.append(new_book)
            with open(self.__files[0], mode='a', newline='') as b_csv:
                writer = csv.writer(b_csv)
                writer.writerow([title, author, available_copies, total_books, genre, year, popularity])
            # self.add_to_available_csv(new_book, available_copies)
            print(f"Book added: {new_book}")
        else:
            print("the book already exists")

    def add_user(self, name, username, role, password):
        from src.main_lib.Users import User
        User(name, username, role, password)

    def add_client(self, client):
        Subject.sub(self, client)

    def remove_client(self, client):
        Subject.unsubscribe(self,client)

    def rent_book(self,book):
        rentals = Rentals.get_instance()
        rentals.rent_books(book)
    def return_book(self, book):
        rentals = Rentals.get_instance()
        rentals.return_book(book)

if __name__ == '__main__':
    # books_library = Library.get_instance()
    # book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925)
    # book2 = Books("To Kill a Mockingbird", "Harper Lee", "Yes", 5, "Fiction", 1960)
    # book3 = Books("1984", "George Orwell", "No", 7, "Dystopian", 1949)
    # print("Adding books to available_books.csv:")
    # books_library.add_to_available_csv(book1, 2)
    # books_library.add_to_available_csv(book2, 1)
    # books_library.add_to_available_csv(book3, 1)
    #
    # print("\nCurrent Library:")
    # print()
    # print("\nRemoving a book from available_books.csv:")
    # books_library.remove_from_available_csv(book1)
    # print("\nCheck the files for updates.")

    file_path = os.path.join(os.path.dirname(__file__), 'Excel_Tables/books.csv')
    file_path = os.path.abspath(file_path)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    df = pd.read_csv(file_path)
    s=SearchBooks()
    print()
    s.set_strategy("title")
    print(s.search("nd"))
    print()
    s.set_strategy("author")
    print(s.search("lom"))
    print()
    s.set_strategy("year")
    print(s.search(1999))
    print()
    s.set_strategy("GENRE")
    print(s.search("Drama"))
    print()

