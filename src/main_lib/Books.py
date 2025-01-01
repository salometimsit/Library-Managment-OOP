import csv
import os
from src.main_lib.Excel_Tables import *
class Books:
    # this is a factory class
    def __init__(self, title, author, year, genre, total_books, available_copies):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.total_books = total_books
        self.available_copies = available_copies

    @staticmethod
    def create_book(self):
        return Books(self.title, self.author, self.year, self.genre, self.total_books, self.available_copies)

    def add_to_library(self):
        file_path = "./src/Excel_Tables/books.csv"
        try:
            # Open the file in append mode
            with open(file_path, mode='a') as file:
                writer = csv.writer(file)
                # Append book details to the existing file
                writer.writerow([
                    self.title, self.author, self.year, self.genre,
                    self.total_books, self.available_copies
                ])
            print(f"Book added: {self.title}")
        except Exception as e:
            print(f"Failed to add book {self.title}: {e}")

        # add the book to file of total copies

    def remove_from_library(self):
        if self.T_copies > 0:
            self.T_copies -= 1
            if self.Ava_copies > 0:
                self.Ava_copies -= 1
        else:
            print("No copies left to remove.")

    def borrow_book(self):
        if self.availible_copies > 0:
            self.availible_copies -= 1
        else:
            print("No available books left to remove")

    def return_book(self):
        if self.availible_copies < self.total_books:
            self.availible_copies += 1
        else:
            print("All copies are in the library.")

    def __str__(self):
        return (
            f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "f"Genre: {self.genre}, Total Copies: {self.total_books}, "
            f"Available Copies: {self.available_copies}")
