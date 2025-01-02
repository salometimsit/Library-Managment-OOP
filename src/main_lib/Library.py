import csv
import os
from src.main_lib.Books import Books
from src.main_lib.Subject import Subject
from src.main_lib.Users import User


class Library(Subject):
    __instance = None

    # נסיון
    def __init__(self):
        super().__init__()
        if Library.__instance is None:
            # Path to books.csv inside Excel_Tables under main_lib
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv']
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

    def add_book(self, title, author, total_books, available_copies, genre, year):
        # Use the factory method to create a new book
        flag = True
        new_book = Books.create_book(title, author, total_books, available_copies, genre, year)
        for book in self.books:
            if new_book.compare_books(book):
                flag = False
        if flag:
            self.books.append(new_book)

            # Append to CSV file
            with open(self.files[0], mode='a', newline='') as b_csv:
                writer = csv.writer(b_csv)
                writer.writerow([new_book.__title, new_book.__author, new_book.__total_books,
                                 new_book.__is_loaned, new_book.__genre, new_book.__year])
            print(f"Book added: {new_book}")
        else:
            print("the book already exists")

    def add_user(self, name, username, role, password):
        User(name, username, role, password)

    def add_client(self, client):
        Subject.sub(self, client)

    def remove_client(self, client):
        Subject.unsubscribe(self, client)

    def add_to_available_csv(self, book, available_copies):
        if book.available_to_loan():
            with open(self.files[1], mode='a', newline='') as b_csv:
                writer = csv.writer(b_csv)
                writer.writerow([book.get_title(), book.get_author(), available_copies,
                                 book.get_genre(), book.get_year()])


if __name__ == '__main__':
    books_library = Library.get_instance()
    print(books_library)
    # Add a new book using the factory method
    books_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 10, 'NO', "Fiction", 1925)
    books = books_library.get_books()
    for book in books:
        books_library.add_to_available_csv(book, 1)
    print("\n\n")
    print(books_library)
