import os
from zoneinfo import available_timezones

import pandas as pd
from src.main_lib.Books import Books
from src.main_lib.BooksCategory import BooksCategory

from src.main_lib.Search_Books import SearchBooks


class BooksFactory:
    def __init__(self,files):
        self.searcher = SearchBooks().set_strategy("title")
        self.__files = files

    def create_in_bookscsv(self,title, author, copies,genre,year):
        df = pd.read_csv(self.__files[0])
        filtered_df = df[(df['author'] == author) & (df['title'] == title) &
                         (df['genre'] == genre) & (df['year'] == year)]

        if not filtered_df.empty:
            df.loc[(df['author'] == author) & (df['title'] == title) &
                   (df['genre'] == genre) & (df['year'] == year), "copies"] += int(copies)
            df.loc[(df['author'] == author) & (df['title'] == title) &
                   (df['genre'] == genre) & (df['year'] == year), "is_loaned"] = "No"

        else:
            new_book = Books(title, author, "No", int(copies), genre, year, 0)
            df = pd.concat([df, pd.DataFrame([new_book.to_dict()])], ignore_index=True)

        book = df.loc[(df['author'] == author) & (df['title'] == title) &
                      (df['genre'] == genre) & (df['year'] == year)]
        df.to_csv(self.__files[0], index=False)
        return book

    def add_to_available(self,title,author,copies,genre,year,book):
        available_df = pd.read_csv(self.__files[1])
        filtered_available_df = available_df[(available_df['author'] == author) &
                                             (available_df['title'] == title) &
                                             (available_df['genre'] == genre) &
                                             (available_df['year'] == year)]

        if not filtered_available_df.empty:

            available_df.loc[(available_df['author'] == author) & (available_df['title'] == title)
                             & (available_df['genre'] == genre) & (available_df['year'] == year),
            "copies"] += copies
        else:
            new_available_book = {"title": title, "author": author, "is_loaned": "No", "copies": copies
                , "genre": genre, "year": year, "popularity": book["popularity"].values[0]}
            available_df = pd.concat([available_df, pd.DataFrame([new_available_book])], ignore_index=True)
        available_df.to_csv(self.__files[1], index=False)

    def check_not_available(self,title,author,genre,year):
        not_available_df = pd.read_csv(self.__files[2])
        filtered_non_available_df = not_available_df[(not_available_df['author'] == author) &
                                             (not_available_df['title'] == title) &
                                             (not_available_df['genre'] == genre) &
                                             (not_available_df['year'] == year)]
        if not filtered_non_available_df.empty:
            not_available_df.loc[(not_available_df['author'] == author) & (not_available_df['title'] == title)
                             & (not_available_df['genre'] == genre) & (not_available_df['year'] == year),
            "is_loaned"] ="No"
        not_available_df.to_csv(self.__files[2], index=False)


    def create_books(self,title, author, copies,genre,year):
        if(copies <=0):
            return None
        if genre not in BooksCategory._value2member_map_:
            print("Genre is not a valid genre")
            return None
        book=self.create_in_bookscsv(title, author, copies,genre,year)
        self.add_to_available(title,author,copies,genre,year,book)
        self.check_not_available(title, author, genre, year)
        if book["copies"].values[0]==copies:
            return True
        return False


if __name__ == '__main__':
    filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                 'Excel_Tables/not_available_books.csv']
    __files = []
    for filename in filenames:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        file_path = os.path.abspath(file_path)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        __files.append(file_path)
    b=BooksFactory(__files)
    ans=b.create_books("To Kill a Mockingbird","Harper Lee", 5,"Fiction",1960)
    ans2=b.create_books("Pride and Prejudice","Jane Austen",2,"Romance",1813)
    ans3=b.create_books("salome timsit life story","salome timsit",3,"Realism",2002)
    print(ans)
    print(ans2)
    print(ans3)
