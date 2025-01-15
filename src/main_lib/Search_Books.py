
import pandas as pd

from src.main_lib.FilesHandle import FilesHandle
from src.main_lib.SearchStrategy import SearchStrategy, TitleSearch, AuthorSearch, YearSearch, GenreSearch


class SearchBooks:
    """
    Handles the search functionality for books in the library system.

    Attributes:
        __strategy (SearchStrategy): The current search strategy to be used.
        __title_strategy (TitleSearch): Strategy for searching by title.
        __author_strategy (AuthorSearch): Strategy for searching by author.
        __year_strategy (YearSearch): Strategy for searching by year.
        __genre_strategy (GenreSearch): Strategy for searching by genre.
    """

    def __init__(self):
        """
        Initializes the SearchBooks instance and sets up all available strategies.
        """
        self.__strategy = None
        self.__title_strategy = TitleSearch()
        self.__author_strategy = AuthorSearch()
        self.__year_strategy = YearSearch()
        self.__genre_strategy = GenreSearch()
        self.__files = FilesHandle().get_file_by_category("book")

    def set_strategy(self, strategy):
        """
        Sets the search strategy based on the given input.

        Args:
            strategy (str): The type of search strategy ('title', 'author', 'year', 'genre').

        Raises:
            Exception: If the strategy type is invalid.
        """
        strategy=strategy.lower()
        if strategy == "title":
            self.__strategy = self.__title_strategy
        elif strategy== 'author':
            self.__strategy = self.__author_strategy
        elif strategy == 'year':
            self.__strategy = self.__year_strategy
        elif strategy == 'genre':
            self.__strategy = self.__genre_strategy
        else:
            raise Exception('Invalid strategy')

    def search_all(self, name):
        df = pd.read_csv(self.__files[0])
        return self.__strategy.search(df, name)

    def search_loaned(self,name):
        df = pd.read_csv(self.__files[2])
        return self.__strategy.search(df, name)

    def search_available(self,name):
        df = pd.read_csv(self.__files[1])
        return self.__strategy.search(df, name)

