
class SearchStrategy:
    def search(self,df,value):
        raise NotImplementedError("Every SubClass must implement this method")

class TitleSearch(SearchStrategy):
    def search(self, df,value):
        return df[df['title'].str.contains(value,case=False, na=False)]

class AuthorSearch(SearchStrategy):
    def search(self, df,value):
        return df[df['author'].str.contains(value,case=False, na=False)]

class YearSearch(SearchStrategy):
    def search(self, df,value):
        return df[df['year'].astype(str)==str(value)]

class GenreSearch(SearchStrategy):
    def search(self, df,value):
        return df[df['genre'].str.contains(value,case=False,na=False)]

