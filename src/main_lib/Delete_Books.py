import os
from re import search

import pandas as pd

from src.main_lib.Logger import Logger
from src.main_lib.Search_Books import SearchBooks


class DeleteBooks:
    filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                 'Excel_Tables/not_available_books.csv']
    __files = []
    for filename in filenames:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        __files.append(file_path)

    @staticmethod
    def delete_books(book):
        sb = SearchBooks()
        sb.set_strategy("title")
        l_dict = sb.search_loaned(book.get_title())
        if not len(l_dict) == 0:
            raise Exception("Delete failed, book is currently borrowed.")

        try:
            df_not_available = pd.read_csv(DeleteBooks.__files[2])  # not_available_books.csv
            match = df_not_available[
                (df_not_available['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df_not_available['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df_not_available['year'].astype(int) == int(book.get_year()))
                ]
            if not match.empty:
                raise Exception("Delete failed, book is not available and cannot be removed.")
        except FileNotFoundError:
            raise FileNotFoundError("Not available books file not found.")
        except Exception as e:
            raise Exception(f"Error while checking not available books: {e}")

        try:
            df_books = pd.read_csv(DeleteBooks.__files[0])
            df_available = pd.read_csv(DeleteBooks.__files[1])

            book_in_books = df_books[
                (df_books['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df_books['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df_books['year'].astype(int) == int(book.get_year()))
                ]

            book_in_available = df_available[
                (df_available['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df_available['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df_available['year'].astype(int) == int(book.get_year()))
                ]

            if book_in_books.empty and book_in_available.empty:
                raise Exception("Delete failed, book not found in books or available books.")

            if not book_in_books.empty:
                DeleteBooks.delete_from_csv(DeleteBooks.__files[0], book)

            if not book_in_available.empty:
                DeleteBooks.delete_from_csv(DeleteBooks.__files[1], book)
            return True

        except Exception:
            raise Exception("Delete failed, book could not be deleted.")

    @staticmethod
    def delete_from_csv(file,book):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if match.empty:
                print(f"Book '{book.get_title()}' not found in {file}.")
            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                      (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(file, index=False)
            print(f"Book '{book.get_title()}' removed from {file}.")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")





