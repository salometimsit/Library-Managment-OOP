import csv
import os

class Books:
    # this is a factory class
    # title, author, is_loaned, copies, genre, year
    def __init__(self, title, author, total_books, available_copies, genre, year):
        self.title = title
        self.author = author
        self.total_books = total_books
        self.available_copies = available_copies
        self.genre = genre
        self.year = year

    @staticmethod
    def create_book(title, author, total_books, available_copies, genre, year):
        """Factory method to create and return a Books instance"""
        return Books(title, author, total_books, available_copies, genre, year)

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_year(self):
        return self.year

    def get_genre(self):
        return self.genre

    def get_total_books(self):
        return self.total_books

    def get_available_copies(self):
        return self.available_copies

    def add_to_library(self):
        """Append book details to the CSV file"""
        file_path = "./src/main_lib/Excel_Tables/books.csv"  # Adjusted to your directory
        try:
            with open(file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    self.title, self.author, self.total_books,
                    self.available_copies, self.genre, self.year
                ])
            print(f"Book added to library: {self.title}")
        except Exception as e:
            print(f"Failed to add book {self.title}: {e}")

    def remove_from_library(self):
        """Logic for removing a book - requires implementation"""
        if self.total_books > 0:
            self.total_books -= 1
            if self.available_copies > 0:
                self.available_copies -= 1
        else:
            print("No copies left to remove.")

    def borrow_book(self):
        """Decrease the available copies if one is borrowed"""
        if self.available_copies > 0:
            self.available_copies -= 1
        else:
            print("No available copies to borrow.")

    def return_book(self):
        """Increase the available copies if one is returned"""
        if self.available_copies < self.total_books:
            self.available_copies += 1
        else:
            print("All copies are already in the library.")

    def __str__(self):
        """String representation of the book"""
        return (
            f"Title: {self.title}, Author: {self.author}, Available Copies: {self.available_copies}, "
            f"Total Copies: {self.total_books}, Genre: {self.genre}, Year: {self.year}"
        )
