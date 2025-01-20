from src.main_lib.BooksFactory import BooksFactory
from src.main_lib.Logger import Logger


class Factory_of_Items:
    """
    A factory class to handle the creation of book items.
    """
    @staticmethod
    def factory_of_items(types, title, author, copies, genre, year,files):
        """
        Getting parameters of item and creating him
        """
        def normalize_spaces(text):
            return ' '.join(str(text).split())

        if not normalize_spaces(title) or not normalize_spaces(author) or not normalize_spaces(genre):
            return None
        if not isinstance(copies, (int, float)) or not isinstance(year, (int, float)):
            return None

        if types.lower() == "book":
            book_files=[]
            for file in files:
                if "book" in file.lower():
                    book_files.append(file)
            return Factory_of_Items.__add_book(title, author, copies, genre, year,files)
        return None


    @staticmethod
    @Logger.log_method_call("Add book")
    def __add_book(title, author, copies, genre, year,files):
        """
        Private method to create a book instance using BooksFactory.
        """
        facbooks=BooksFactory(files)
        return facbooks.create_books(title, author, copies, genre, year)
