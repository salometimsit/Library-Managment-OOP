from src.main_lib.BooksFactory import BooksFactory
from src.main_lib.Logger import Logger


class Factory_of_Items:
    """
    A factory class to handle the creation of book items.
    """
    @staticmethod
    def factory_of_items(types, title, author, copies, genre, year,files):
        if types == "Book":
            book_files=[]
            for file in files:
                if "book" in file.lower():
                    book_files.append(file)
            return Factory_of_Items.__add_book(title, author, copies, genre, year,files)


    @staticmethod
    @Logger.log_method_call("Add book")
    def __add_book(title, author, copies, genre, year,files):
        """
        Private method to create a book instance using BooksFactory.
        """
        facbooks=BooksFactory(files)
        return facbooks.create_books(title, author, copies, genre, year)
