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
        """
        Initializes the library instance, loading necessary files and setting up services.
        """
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
        """
        Retrieves the singleton instance of the library.

        Returns:
            Library: The singleton library instance.
        """
        if Library.__instance is None:
            Library.__instance = Library()
        return Library.__instance

    def set_current_librarian(self, librarian):
        """
       Sets the current librarian and subscribes them for notifications.

       Args:
           librarian (User): The librarian to set as current.
       """
        self.current_librarian = librarian
        self._sub=[]
        if librarian and librarian.get_role() == "librarian":
            self.subscribe(librarian)
            self._sub.append(librarian)

    def get_rentals(self):
        """
        Retrieves the rentals service from the service locator.

        Returns:
            Rentals: The rentals service instance.
        """
        return LibraryServiceLocator.get_rentals()

    @Logger.log_method_call("logged in")
    def user_login(self, username, password):
        """
        Logs in a user if credentials are correct.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if login is successful, False otherwise.
        """
        user = next((u for u in self.users if u.get_username() == username), None)
        if user and user.check_password(password):
            self.current_librarian = user
            self.subscribe(user)
            return True
        return False

    def check_login(self):
        """
        Checks if a librarian is currently logged in.

        Returns:
            bool: True if a librarian is logged in, False otherwise.
        """
        if self.current_librarian is None:
            return False
        return True


    @Logger.log_method_call("log out")
    def user_register(self, fullname, username, password):
        """
        Registers a new user.

        Args:
            fullname (str): The full name of the user.
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        if any(u.get_username() == username for u in self.users):
            return False
        else:
            self.add_user(fullname,username,"librarian",password)
            return True

    def user_logout(self):
        """
       Logs out the current librarian.

       Returns:
           bool: True if logout is successful, False otherwise.
       """
        if self.current_librarian is not None:
            self.unsubscribe(self.current_librarian)
            self.current_librarian=None
            Logger.log_add_message("log out successful") #here we added it manually cause the message is successful
            return True
        else:
            Logger.log_add_message("log out fail")
            return False


    def add_item(self,types, title, author, copies, genre, year):
        """
        Adds an item to the library.
        Returns:
            bool: True if item was added, False otherwise.
        """
        return Factory_of_Items.factory_of_items(types, title, author, copies, genre, year, self.__book_files)

    @Logger.log_method_call("book removed")
    def delete_book(self, book):
        """
        Deletes a book from the library.
        Returns:
            bool: True if the book was deleted successfully, False otherwise.
        """
        try:
            return DeleteBooks.delete_books(book)
        except Exception:
            return False

    def add_user(self, name, username, role, password):
        """
       Adds a new user to the library system.
       """
        new_user=User(name, username, role, password)
        self.users.append(new_user)
        if role == "librarian":
            self.subscribe(new_user)

    def rent_book(self, book):
        """
       Rents a book to a user.
       Returns:
           bool: True if the book was rented successfully, False otherwise.
       """
        rentals = self.get_rentals()
        return rentals.rent_books(book)

    def return_book(self, book):
        """
        gives back a rented book to the library.
        Returns:
            bool: True if the book was returned successfully, False otherwise.
        """
        rentals = self.get_rentals()
        return rentals.return_books(book)

    @Logger.log_method_call("Displayed all books")
    def display_all_books(self):
        """
        Displays all books in the library.
        Returns:
            list: A list of dictionaries representing all books.
        Raises:
            FileNotFoundError: If the books file is not found or is empty.
        """
        df = pd.read_csv(self.__book_files[0])
        if df.empty:
            raise FileNotFoundError("File not found")
        return df.to_dict(orient='records')

    @Logger.log_method_call("Displayed borrowed books")
    def display_not_available_books(self):
        """
       Displays books that are currently loaned out.
       Returns:
           list: A list of dictionaries representing loaned books.
       Raises:
           FileNotFoundError: If the loaned books file is not found or is empty.
       """
        df = pd.read_csv(self.__book_files[2])
        if df.empty:
            raise FileNotFoundError("File not found")
        return df.to_dict(orient='records')

    @Logger.log_method_call("Displayed available books")
    def display_available_books(self):
        """
       Displays books that are currently available in the library.
       Returns:
           list: A list of dictionaries representing available books.
       Raises:
           FileNotFoundError: If the available books file is not found or is empty.
       """
        df = pd.read_csv(self.__book_files[1])
        if df.empty:
            raise FileNotFoundError("File not found")
        return df.to_dict(orient='records')

    @Logger.log_method_call("Displayed popular books")
    def display_popular_books(self):
        """
       Displays the top 10 most popular books in the library.

       Returns:
           list: A list of dictionaries representing the top 10 most popular books.

       Raises:
           FileNotFoundError: If the books file is not found or is empty.
           KeyError: If the 'popularity' column is not found in the dataset.
       """
        df = pd.read_csv(self.__book_files[0])
        if df.empty:
            raise FileNotFoundError("File not found")
        if 'popularity' not in df.columns:
            raise KeyError("Column 'popularity' not found in the dataset")
        top_10_books = df.sort_values(by='popularity', ascending=False).head(10)
        return top_10_books.to_dict(orient='records')

    @Logger.log_method_call("Displayed category books")
    def display_genre(self, category):
        """
        Displays books by genre.
        Returns:
            list: A list of books in the specified genre.
        """
        self.searcher.set_strategy("genre")
        result=self.searcher.search_all(category)
        if result== []:
            return []
        else:
            return result


    def search_book(self, name, strategy):
        """
      Searches for books using a specified strategy.
      Returns:
          list: A list of books matching the search criteria.
      """
        self.searcher.set_strategy(strategy)
        df = self.searcher.search_all(name)
        if df == []:
            if strategy.lower() != "year":
                Logger.log_add_message(f"Search book '{name}' by {strategy} name completed fail")
            else:
                Logger.log_add_message(f"Search book '{name}' by {strategy} completed fail")
        else:
            if strategy.lower() != "year":
                Logger.log_add_message(f"Search book '{name}' by {strategy} name completed successfully")
            else:
                Logger.log_add_message(f"Search book '{name}' by {strategy} completed successfully")
        return df

    def add_to_waiting_list(self, book,name,phone,email):
        """
       Adds a user to the waiting list for a book.

       Returns:
           bool: True if the user was added successfully, False otherwise.
       """
        return Rentals.get_instance().add_to_waiting_list(book, name, phone,email)

    def get_books_category(self):
        """
       Retrieves the BooksCategory class.

       Returns:
           type: The BooksCategory class.
       """
        return BooksCategory

    def get_book(self,title,author,is_loaned,total_books,genre,year,popularity):
        """
          Creates a Books instance.

          Returns:
              Books: The created Books instance.
          """
        return Books(title=title,author=author,is_loaned=is_loaned,total_books=total_books
                     ,genre=genre,year=year,popularity=popularity)


    def notify(self, message):
        """
        Sends a notification to the current librarian.
        """

        if hasattr(self, 'current_librarian') and self.current_librarian:
            if self.current_librarian not in self._sub:
                self._sub = []
                self.subscribe(self.current_librarian)
            self.current_librarian.update(self, message)

