
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
        raise NotImplementedError("Every SubClass must implement this method")

class TitleSearch(SearchStrategy):
    def search(self, df,value):
        lst = []
        it = BookIterator(df, column="title", value=value)
        for b in it:
            lst.append(b)
        return lst


class AuthorSearch(SearchStrategy):
    def search(self, df,value):
        lst = []
        it = BookIterator(df, column="author", value=value)
        for b in it:
            lst.append(b)
        return lst

class YearSearch(SearchStrategy):
    def search(self, df,value):
        lst = []
        it = BookIterator(df, column="year", value=value)
        for b in it:
            lst.append(b)
        return lst

class GenreSearch(SearchStrategy):
    def search(self, df,value):
        lst = []
        it = BookIterator(df, column="genre", value=value)
        for b in it:
            lst.append(b)
        return lst