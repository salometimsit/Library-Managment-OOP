import os
import pandas as pd

from src.main_lib.SearchStrategy import SearchStrategy, TitleSearch, AuthorSearch, YearSearch, GenreSearch


class SearchBooks:
    def __init__(self):
        self.__strategy=None
        self.__title_strategy=TitleSearch()
        self.__author_strategy=AuthorSearch()
        self.__year_strategy=YearSearch()
        self.__genre_strategy=GenreSearch()

    def set_strategy(self, strategy):
        if strategy.lower() == "title":
            self.__strategy = TitleSearch()
        elif strategy.lower() == 'author':
            self.__strategy = AuthorSearch()
        elif strategy.lower() == 'year':
            self.__strategy = YearSearch()
        elif strategy.lower() == 'genre':
            self.__strategy = GenreSearch()
        else:
            raise Exception('Invalid strategy')


    def search(self, name):
        file_path = os.path.join(os.path.dirname(__file__), 'Excel_Tables/books.csv')
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        df = pd.read_csv(file_path)
        return self.__strategy.search(df, name)



