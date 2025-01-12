import pandas as pd
class BookIterator:
    def __init__(self, df,column=None,value=None):
        if column and value:
            self.df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
            self.index = 0
            if df.empty:
                raise Exception(f"Search {value} by {column} failed")
        else:
            raise Exception(f"Search {value} by {column} failed")

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.df):
            raise StopIteration
        book = self.df.iloc[self.index]
        self.index += 1
        return book.to_dict()
