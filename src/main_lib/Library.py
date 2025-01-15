import pandas as pd
from src.main_lib.Books import Books
from src.main_lib.BooksCategory import BooksCategory
from src.main_lib.Factory_of_Items import Factory_of_Items
from src.main_lib.FilesHandle import FilesHandle
from src.main_lib.LibraryServiceLocator import LibraryServiceLocator
from src.main_lib.Logger import Logger
from src.main_lib.BooksFactory import BooksFactory
from src.main_lib.Delete_Books import DeleteBooks
from src.main_lib.Rentals import Rentals
from src.main_lib.Search_Books import SearchBooks
from src.main_lib.Subject import Subject
from src.main_lib.Users import User


class Library(Subject):
    """
    Represents a library system to manage books, users, and rentals.
    Implements the Singleton pattern.

    Attributes:
        __instance (Library): Singleton instance of the Library class.
        __book_files (list): List of file paths for books, available_books, and not_available_books CSV files.
    """

    __instance = None

    def __init__(self):
        if Library.__instance is None:
            super().__init__()
            self.searcher = SearchBooks()
            self.__files= FilesHandle().get_all_files()
            self.__book_files = FilesHandle.get_file_by_category("book")
            self.facbooks = BooksFactory(self.__book_files)
            LibraryServiceLocator.set_library(self)
            from src.main_lib.Rentals import Rentals
            Rentals.get_instance()
            self.current_librarian=None
            self.users=User.get_all_users()



    @staticmethod
    def get_instance():
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def set_current_librarian(self, librarian):
        self.current_librarian = librarian
        self.sub=[]
        if librarian and librarian.get_role() == "librarian":
            self.subscribe(librarian)
            self.sub.append(librarian)

    def get_rentals(self):
        return LibraryServiceLocator.get_rentals()

    @Logger.log_method_call("Logged in")
    def user_login(self, username, password):
        user = next((u for u in self.users if u.get_username() == username), None)
        if user and user.check_password(password):
            self.current_librarian = user
            self.subscribe(user)
            return True
        return False

    def check_login(self):
        if self.current_librarian is None:
            return False
        return True


    @Logger.log_method_call("Logged out")
    def user_register(self, fullname, username, password):
        if any(u.get_username() == username for u in self.users):
            return False
        else:
            self.add_user(fullname,username,"librarian",password)
            return True

    @Logger.log_method_call("Logged out")
    def user_logout(self):
        if self.current_librarian is not None:
            self.current_librarian=None
            return True
        else:
            return False


    def add_item(self,type, title, author, copies, genre, year):
        return Factory_of_Items.factory_of_items(type, title, author, copies, genre, year, self.__book_files)

    @Logger.log_method_call("book removed")
    def delete_book(self, book):
        try:
            return DeleteBooks.delete_books(book)
        except Exception:
            return False

    def add_user(self, name, username, role, password):
        new_user=User(name, username, role, password)
        self.users.append(new_user)
        if role == "librarian":
            self.subscribe(new_user)


    def rent_book(self, book):
        rentals = self.get_rentals()
        return rentals.rent_books(book)


    def return_book(self, book):
        rentals = self.get_rentals()
        return rentals.return_books(book)

    def display_all_books(self):
        df = pd.read_csv(self.__book_files[0])
        if df.empty:
            Logger.log_add_message("Displayed all books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed all books successfully")
        return df.to_dict(orient='records')

    def display_not_available_books(self):
        df = pd.read_csv(self.__book_files[2])
        if df.empty:
            Logger.log_add_message("Displayed borrowed books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed borrowed books successfully")
        return df.to_dict(orient='records')

    def display_available_books(self):
        df = pd.read_csv(self.__book_files[1])
        if df.empty:
            Logger.log_add_message("Displayed available books fail")
            raise FileNotFoundError("File not found")
        Logger.log_add_message("Displayed available books successfully")
        return df.to_dict(orient='records')

    def display_popular_books(self):
        df = pd.read_csv(self.__book_files[0])
        if df.empty:
            Logger.log_add_message("Displayed popular books fail")
            raise FileNotFoundError("File not found")
        if 'popularity' not in df.columns:
            Logger.log_add_message("Displayed popular books fail")
            raise KeyError("Column 'popularity' not found in the dataset")
        top_10_books = df.sort_values(by='popularity', ascending=False).head(10)
        Logger.log_add_message("Displayed popular books successfully")
        return top_10_books.to_dict(orient='records')

    def display_genre(self, category):
        self.searcher.set_strategy("genre")
        result=self.searcher.search_all(category)
        if result== []:
            Logger.log_add_message("Displayed category fail")
            return []
        else:
            Logger.log_add_message("Displayed category successfully")
            return result


    def search_book(self, name, strategy):
        self.searcher.set_strategy(strategy)
        df = self.searcher.search_all(name)
        if df == []:
            Logger.log_add_message(f"Search book '{name}' by {strategy} name completed fail")
        else:
            Logger.log_add_message(f"Search book '{name}' by {strategy} name completed successfully")
        return df

    def add_to_waiting_list(self, book,name,phone,email):
        return Rentals.get_instance().add_to_waiting_list(book, name, phone,email)

    def get_books_category(self):
        return BooksCategory

    def get_book(self,title,author,is_loaned,total_books,genre,year,popularity):
        return Books(title=title,author=author,is_loaned=is_loaned,total_books=total_books
                     ,genre=genre,year=year,popularity=popularity)


    def notify(self, message):
        if hasattr(self, 'current_librarian') and self.current_librarian:
            if self.current_librarian not in self.sub:
                self.sub = []
                self.subscribe(self.current_librarian)
            self.current_librarian.update(self, message)

