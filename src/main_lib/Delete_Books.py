
import pandas as pd

from src.main_lib.FilesHandle import FilesHandle


class DeleteBooks:
    """
    This class dealing with the deletion of books from the library
    """
    @staticmethod
    def delete_books(book):
        """
        This function deletes the books from the library by cheking if they are exist and no loaned
        :param book:
        :return:
        """
        def normalize_spaces(text):
            return ' '.join(str(text).split())
        __files = FilesHandle().get_file_by_category("book")
        try:
            df_not_available = pd.read_csv(__files[2])
            match = df_not_available[
                (df_not_available['title'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_title()).strip().lower()) &
                (df_not_available['author'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_author()).strip().lower()) &
                (df_not_available['year'].astype(int) == int(book.get_year()))&
                (df_not_available['genre'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_genre()).strip().lower())
                ]
            if not match.empty:
                raise Exception("Delete failed, book is not available and cannot be removed.")
        except FileNotFoundError:
            raise FileNotFoundError("Not available books file not found.")
        except Exception as e:
            raise Exception(f"Error while checking not available books: {e}")

        try:
            df_books = pd.read_csv(__files[0])
            df_available = pd.read_csv(__files[1])

            book_in_books = df_books[
                (df_books['title'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_title()).strip().lower()) &
                (df_books['author'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_author()).strip().lower()) &
                (df_books['year'].astype(int) == int(book.get_year())) &
                (df_books['genre'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_genre()).strip().lower())]

            book_in_available = df_available[
                (df_available['title'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_title()).strip().lower()) &
                (df_available['author'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_author()).strip().lower()) &
                (df_available['year'].astype(int) == int(book.get_year())) &
                (df_available['genre'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_genre()).strip().lower())]

            if book_in_books.empty and book_in_available.empty:
                raise Exception("Delete failed, book not found in books or available books.")
            if not book_in_books.empty:
                DeleteBooks.delete_from_csv(__files[0], book)
            if not book_in_available.empty:
                DeleteBooks.delete_from_csv(__files[1], book)
            return True

        except Exception:
            raise Exception("Delete failed, book could not be deleted.")

    @staticmethod
    def delete_from_csv(file, book):
        """
        This method deletes the book from a given csv file
        """
        def normalize_spaces(text):
            return ' '.join(str(text).split())
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_title()).strip().lower()) &
                       (df['author'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_author()).strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))&
                        (df['genre'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_genre()).strip().lower())]

            if match.empty:
                print(f"Book '{book.get_title()}' not found in {file}.")

            df = df[~((df['title'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_title()).strip().lower()) &
                      (df['author'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_author()).strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year()))&
                    (df['genre'].apply(normalize_spaces).str.lower() == normalize_spaces(book.get_genre()).strip().lower()))]

            df.to_csv(file, index=False)

        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")
