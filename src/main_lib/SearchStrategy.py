
"""
These classes implement 4 search strategies for Books:
Search by Title
Search by Author
Search by Year
Search by Publisher
"""
from src.main_lib.BookIterator import BookIterator


class SearchStrategy:
    def search(self,df,value):
        """
        Abstract method for performing a search.
        Args:
            df (DataFrame): The DataFrame containing book data.
            value (str): The value to search for in the DataFrame..
        """
        raise NotImplementedError("Every SubClass must implement this method")

class TitleSearch(SearchStrategy):
    def search(self, df,value):
        """
        Searches for books by title.

        Args:
             df (DataFrame): The DataFrame containing book data.
            value (str): The title to search for.

        Returns:
            list: A list of books that match the title.
         """
        lst = []
        it = BookIterator(df, column="title", value=value)
        for b in it:
            lst.append(b)
        return lst


class AuthorSearch(SearchStrategy):
    def search(self, df,value):
        """
        Searches for books by author.

        Args:
            df (DataFrame): The DataFrame containing book data.
            value (str): The author to search for.

        Returns:
            list: A list of books that match the given author.
        """
        lst = []
        it = BookIterator(df, column="author", value=value)
        for b in it:
            lst.append(b)
        return lst

class YearSearch(SearchStrategy):
    def search(self, df,value):
        """
        Searches for books by year.

        Args:
            df (DataFrame): The DataFrame containing book data.
            value (str): The year to search for.

        Returns:
            list: A list of books that match the given year.
        """
        lst = []
        it = BookIterator(df, column="year", value=value)
        for b in it:
            lst.append(b)
        return lst

class GenreSearch(SearchStrategy):
    def search(self, df,value):
        """
       Searches for books by genre.

       Args:
           df (DataFrame): The DataFrame containing book data.
           value (str): The genre to search for.

       Returns:
           list: A list of books that match the given genre.
       """
        lst = []
        it = BookIterator(df, column="genre", value=value)
        for b in it:
            lst.append(b)
        return lst