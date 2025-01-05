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
        flag = True
        new_book = Books.create_book(title, author, available_copies,total_books, genre, year)
        for book in self.books:
            if new_book.compare_books(book):
                flag = False
        if flag:
            self.books.append(new_book)
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
        try:
            if self.find_in_csv(book) is None:
                with open(self.files[1], mode='a', newline='') as av_csv:
                    writer = csv.writer(av_csv)
                    if not os.path.isfile(self.files[1]) or os.path.getsize(self.files[1]) == 0:
                        writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year'])
                    writer.writerow([book.get_title(),book.get_author(),book.get_is_loaned(),available_copies,book.get_genre(),
                        book.get_year()])
                print(f"Book '{book.get_title()}' added to available_books successfully.")
            else:
                print(f"Book '{book.get_title()}' already exists in available_books")
        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def find_in_csv(self, book):
        try:
            df = pd.read_csv(self.files[1])
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                        df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if not match.empty:
                return match.iloc[0].to_dict()
            else:
                return None
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"An error occurred in find_in_csv: {e}")
            return None

    def in_notavailable_book(self, book):
        try:
            df = pd.read_csv(self.files[2])
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year()))]
            if not match.empty:
                if not df[
                    (df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                    (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                    (df['year'].astype(int) == int(book.get_year()))].empty:
                    print(f"Book '{book.get_title()}' already exists in not_available_books.csv.")
                    return  True
            return False
        except FileNotFoundError:
            return None






#MATCH- used to determine if each string in the underlying data of the given series object matches a regular expression
    # def remove_from_available_csv(self, book):
    #     try:
    #         df = pd.read_csv(self.files[1])
    #         match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &(df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
    #             (df['year'].astype(int) == int(book.get_year()))]
    #         if match.empty:
    #             print(f"Book '{book.get_title()}' not found in available_books.csv.")
    #             return
    #         df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &(df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
    #                     (df['year'].astype(int) == int(book.get_year())))]
    #         df.to_csv(self.files[1], index=False)
    #         print(f"Book '{book.get_title()}' removed from available_books.csv.")
    #         if not match.empty:
    #             if os.path.isfile(self.files[2]):
    #                 existing_df = pd.read_csv(self.files[2])
    #                 if not existing_df[
    #                     (existing_df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
    #                     (existing_df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
    #                     (existing_df['year'].astype(int) == int(book.get_year()))].empty:
    #                     print(f"Book '{book.get_title()}' already exists in not_available_books.csv.")
    #                     return
    #             match.to_csv(self.files[2], mode='a', index=False, header=not os.path.isfile(self.files[2]))
    #             print(f"Book '{book.get_title()}' moved to not_available_books.csv successfully.")
    #     except FileNotFoundError:
    #         print("File not found: available_books.csv")
    #     except Exception as e:
    #         print(f"An error occurred while updating the files: {e}")
    def remove_from_available_csv(self, book):
        try:
            df = pd.read_csv(self.files[1])
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                        df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if match.empty:
                print(f"Book '{book.get_title()}' not found in available_books.csv.")
                return
            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                        df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(self.files[1], index=False)
            print(f"Book '{book.get_title()}' removed from available_books.csv.")
            if not match.empty:
                if os.path.isfile(self.files[2]):
                    if self.in_notavailable_book(book):
                        return
                match.to_csv(self.files[2], mode='a', index=False, header=not os.path.isfile(self.files[2]))
                print(f"Book '{book.get_title()}' moved to not_available_books.csv successfully.")
        except FileNotFoundError:
            print("File not found: available_books.csv")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")

if __name__ == '__main__':
    books_library = Library.get_instance()
    book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 10, "Fiction", 1925)
    book2 = Books("To Kill a Mockingbird", "Harper Lee", "Yes", 5, "Fiction", 1960)
    book3 = Books("1984", "George Orwell", "No", 7, "Dystopian", 1949)
    print("Adding books to available_books.csv:")
    books_library.add_to_available_csv(book1, 2)
    books_library.add_to_available_csv(book2, 1)
    books_library.add_to_available_csv(book3, 1)

    print("\nCurrent Library:")
    print()
    print("\nRemoving a book from available_books.csv:")
    books_library.remove_from_available_csv(book1)
    print("\nCheck the files for updates.")
