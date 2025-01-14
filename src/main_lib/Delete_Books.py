# Delete_Books.py
import os
import pandas as pd


class DeleteBooks:
    filenames = [os.path.join('Excel_Tables', 'books.csv'),
                 os.path.join('Excel_Tables', 'available_books.csv'),
                 os.path.join('Excel_Tables', 'not_available_books.csv')]
    __files = []

    for filename in filenames:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        __files.append(file_path)

    @staticmethod
    def delete_books(book):
        try:
            df_not_available = pd.read_csv(DeleteBooks.__files[2])
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
                (df_books['year'].astype(int) == int(book.get_year())) &
                (df_books['genre'].str.strip().str.lower() == book.get_genre().strip().lower())
                ]

            book_in_available = df_available[
                (df_available['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df_available['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df_available['year'].astype(int) == int(book.get_year())) &
                (df_available['genre'].str.strip().str.lower() == book.get_genre().strip().lower())
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
    def delete_from_csv(file, book):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))&
                        (df['genre'].str.strip().str.lower() == book.get_genre().strip().lower())]

            if match.empty:
                print(f"Book '{book.get_title()}' not found in {file}.")

            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                      (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year()))&
                    (df['genre'].str.strip().str.lower() == book.get_genre().strip().lower()))]

            df.to_csv(file, index=False)

        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")