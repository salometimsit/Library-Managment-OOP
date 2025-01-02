import csv
import os

import pandas as pd

from src.main_lib.Books import Books
from src.main_lib.Subject import Subject


class Library(Subject):
    __instance = None

    # נסיון
    def __init__(self):
        from src.main_lib.Books import Books
        super().__init__()
        if Library.__instance is None:
            # Path to books.csv inside Excel_Tables under main_lib
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv','Excel_Tables/not_available_books.csv']
            self.files = []
            for filename in filenames:
                # Path to the file inside Excel_Tables under main_lib
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.files.append(file_path)

            self.books = []
            with open(self.files[0], mode='r') as b_csv:
                reader = csv.reader(b_csv)
                next(reader, None)  # Skip header row
                for row in reader:
                    if len(row) >= 6:
                        self.books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5]))
                    else:
                        print(f"Invalid row: {row}")

    @staticmethod
    def get_instance():
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def __str__(self):
        s=""
        for book in self.books:
            s+=str(book)+"\n"
        return s

    def get_books(self):
        return self.books

    def add_book(self, title, author,  available_copies,total_books, genre, year):
        # Use the factory method to create a new book
        flag = True
        new_book = Books.create_book(title, author, available_copies,total_books, genre, year)
        for book in self.books:
            if new_book.compare_books(book):
                flag = False
        if flag:
            self.books.append(new_book)

            # Append to CSV file
            with open(self.files[0], mode='a', newline='') as b_csv:
                writer = csv.writer(b_csv)
                writer.writerow([new_book.__title, new_book.__author,new_book.__is_loaned, new_book.__total_books,
                                 new_book.__genre, new_book.__year])
            print(f"Book added: {new_book}")
        else:
            print("the book already exists")

    def add_user(self, name, username, role, password):
        from src.main_lib.Users import User
        User(name, username, role, password)

    def add_client(self, client):
        Subject.sub(self, client)

    def remove_client(self, client):
        Subject.unsubscribe(self, client)

    def add_to_available_csv(self, book, available_copies):
        if book.available_to_loan():
            if self.find_in_csv(book) is None:
                with open(self.files[1], mode='a', newline='') as b_csv:
                    writer = csv.writer(b_csv)
                    writer.writerow([book.get_title(),book.get_author(),book.get_is_loaned(),available_copies,book.get_genre(),book.get_year()])

    def find_in_csv(self, book):
        try:
            df = pd.read_csv(self.files[1])
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &(df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df['year'] == book.get_year())]
            if not match.empty:
                return match.iloc[0].to_dict()
            else:
                print(f"Book '{book.get_title()}' not found in available_books.csv.")
                return None
        except FileNotFoundError:
            print("File not found: available_books.csv")
            return None

    def remove_from_available_csv(self, book):
        try:
            df = pd.read_csv(self.files[1])
            print("CSV Data:", df.head())
            match = df[
                (df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df['year'].astype(int) == int(book.get_year()))
                ]

            if match.empty:
                print(f"Book '{book.get_title()}' not found in available_books.csv.")
                return
            df = df[((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &(df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                        (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(self.files[1], index=False)
            match.to_csv(self.files[2], mode='a', index=False)

            print(f"Book '{book.get_title()}' moved to not_available_books.csv successfully.")
        except FileNotFoundError:
            print("File not found: available_books.csv")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")


if __name__ == '__main__':
    books_library = Library.get_instance()

    # Create a few sample books
    book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925)
    book2 = Books("To Kill a Mockingbird", "Harper Lee", "Yes", 5, "Fiction", 1960)
    book3 = Books("1984", "George Orwell", "No", 7, "Dystopian", 1949)

    # Add the books to the library and to the available_books.csv file
    print("Adding books to available_books.csv:")
    books_library.add_to_available_csv(book1, 5)
    books_library.add_to_available_csv(book2, 2)
    books_library.add_to_available_csv(book3, 3)

    # Print the current library (for debugging purposes)
    print("\nCurrent Library:")
    print(books_library)

    # Test removing a book
    print("\nRemoving a book from available_books.csv:")
    books_library.remove_from_available_csv(book1)

    # Check the available_books.csv and not_available_books.csv files
    print("\nCheck the files for updates.")
