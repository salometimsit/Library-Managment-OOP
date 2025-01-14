import pandas as pd
class BookIterator:
    def __init__(self, df,column=None,value=None,filter_conditions=None):
        if column and value:
            self.df = df[df[column].astype(str).str.contains(str(value), case=False, na=False)]
        elif filter_conditions:
            self.df = df.copy()
            for col, val in filter_conditions.items():
                self.df = self.df[self.df[col].astype(str).str.contains(str(val), case=False, na=False)]
        else:
            raise Exception(f"Search {value} by {column} failed")
        self.index = 0
        if df.empty:
            raise Exception(f"Search {value} by {column} failed")

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.df):
            raise StopIteration
        book = self.df.iloc[self.index]
        self.index += 1
        return book.to_dict()
