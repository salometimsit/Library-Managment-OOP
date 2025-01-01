import csv
import os
from Books import Books

class Library:

    #נסיון
    def __init__(self):
        # Path to books.csv inside Excel_Tables under main_lib
        self.filename = os.path.join(os.path.dirname(__file__), 'Excel_Tables/books.csv')
        self.filename = os.path.abspath(self.filename)
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File not found: {self.filename}")

        self.books = []
        with open(self.filename, mode='r') as b_csv:
            reader = csv.reader(b_csv)
            next(reader, None)  # Skip header row
            for row in reader:
                self.books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5]))

    def __str__(self):
        return "\n".join(str(book) for book in self.books)

    def add_book(self, title, author, total_books, available_copies, genre, year):
        # Use the factory method to create a new book
        new_book = Books.create_book(title, author, total_books, available_copies, genre, year)
        self.books.append(new_book)

        # Append to CSV file
        with open(self.filename, mode='a', newline='') as b_csv:
            writer = csv.writer(b_csv)
            writer.writerow([new_book.title, new_book.author, new_book.total_books,
                             new_book.available_copies, new_book.genre, new_book.year])
        print(f"Book added: {new_book}")


if __name__ == '__main__':
    books_library = Library()
    print(books_library)

    # Add a new book using the factory method
    books_library.add_book("The Great Gatsby", "F. Scott Fitzgerald", 10, 'NO', "Fiction", 1925)
    print("\n\n")
    print(books_library)
