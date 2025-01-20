import pandas as pd
from src.main_lib.Books import Books
from src.main_lib.BooksCategory import BooksCategory
from src.main_lib.FilesHandle import FilesHandle
from datetime import datetime
from src.main_lib.Search_Books import SearchBooks


class BooksFactory:
    """
    This class represent a book factory.
    in this factory the book may be created the book or adding copies fo an exist one
    the class taking care for dealing with the waiting lists and more.
    """
    def __init__(self,files):
        self.searcher = SearchBooks().set_strategy("title")
        self.__files = files

    def create_in_bookscsv(self,title, author, copies,genre,year):
        """
        In this method we are creating or updating the new book in the books csv file.
        """
        df = pd.read_csv(self.__files[0])
        filtered_df = df[(df['author'].str.lower() == author.lower()) & (df['title'].str.lower() == title.lower()) &
                         (df['genre'].str.lower() == genre.lower()) & (df['year'] == year)]

        if not filtered_df.empty:
            df.loc[(df['author'].str.lower() == author.lower()) & (df['title'].str.lower() == title.lower()) &
                   (df['genre'].str.lower() == genre.lower()) & (df['year'] == year), "copies"] += int(copies)
            df.loc[(df['author'].str.lower() == author.lower()) & (df['title'].str.lower() == title.lower()) &
                   (df['genre'].str.lower() == genre.lower()) & (df['year'] == year), "is_loaned"] = "No"

        else:
            new_book = Books(title, author, "No", int(copies), genre, year, 0)
            df = pd.concat([df, pd.DataFrame([new_book.to_dict()])], ignore_index=True)

        book = df.loc[(df['author'].str.lower() == author.lower()) & (df['title'].str.lower() == title.lower()) &
                      (df['genre'].str.lower() == genre.lower()) & (df['year'] == year)]
        df.to_csv(self.__files[0], index=False)
        return book

    def add_to_available(self,book):
        """
        In this method we are creating or updating the new book in the available books csv file.
        """
        title=book.get_title()
        author=book.get_author()
        copies=book.get_total_books()
        genre=book.get_genre()
        year=book.get_year()
        not_available_df = pd.read_csv(self.__files[2])
        book_found = not_available_df[(not_available_df['author'].str.lower() == author.lower()) &
                                      (not_available_df['title'].str.lower() == title.lower()) &
                                      (not_available_df['genre'].str.lower() == genre.lower()) &
                                      (not_available_df['year'] == year)]

        if not book_found.empty and 'waiting_list' in book_found.columns:
            waiting_list = book_found['waiting_list'].iloc[0]

            if pd.notna(waiting_list) and waiting_list.strip():
                from src.main_lib.Library import Library
                lib = Library.get_instance()
                temp_book = lib.get_book(title=title,author=author,is_loaned="No",total_books=copies,
                                         genre=genre,year=year,popularity=book.get_popularity()
                )

                waiting_people = waiting_list.split(';')
                copies_used = 0
                copies_left = copies
                updated_list = waiting_people.copy()

                for person in waiting_people:
                    if copies_left <= 0:
                        break

                    name, phone , email= person.split(':')
                    lib.notify(f"The Book '{book.get_title()}' has been returned and should be transferred to {name},\n"
                   f" Phone: {phone} \n Email: {email}")
                    lib.rent_book(temp_book)
                    updated_list.remove(person)
                    copies_left -= 1
                    copies_used += 1

                new_waiting_list = ';'.join(updated_list) if updated_list else ''
                current_copies = int(book_found['copies'].iloc[0])

                not_available_df.loc[book_found.index, 'copies'] = current_copies + copies_used
                not_available_df.loc[book_found.index, 'waiting_list'] = new_waiting_list
                not_available_df.to_csv(self.__files[2], index=False)

                if copies_left == 0:
                    return
                copies = copies_left
        if copies > 0:
            available_df = pd.read_csv(self.__files[1])
            available_book = available_df[(available_df['author'].str.lower() == author.lower()) &
                                          (available_df['title'].str.lower() == title.lower()) &
                                          (available_df['genre'].str.lower() == genre.lower()) &
                                          (available_df['year'] == year)]

            if not available_book.empty:
                available_df.loc[(available_df['author'].str.lower() == author.lower()) &
                                 (available_df['title'].str.lower() == title.lower()) &
                                 (available_df['genre'].str.lower() == genre.lower()) &
                                 (available_df['year'] == year), "copies"] += copies
            else:
                new_book = {"title": title,"author": author,"is_loaned": "No","copies": copies,"genre": genre,
                    "year": year, "popularity": book.get_popularity()
                }
                available_df = pd.concat([available_df, pd.DataFrame([new_book])], ignore_index=True)
            available_df.to_csv(self.__files[1], index=False)

    def check_not_available(self,book):
        """
        In this method we are creating or updating the new book in the not available books csv file.
        """
        title=book.get_title()
        author=book.get_author()
        genre=book.get_genre()
        year=book.get_year()
        not_available_df = pd.read_csv(self.__files[2])
        filtered_non_available_df = not_available_df[(not_available_df['author'].str.lower() == author.lower()) &
                                             (not_available_df['title'].str.lower() == title.lower()) &
                                             (not_available_df['genre'].str.lower() == genre.lower()) &
                                             (not_available_df['year'] == year)]
        if not filtered_non_available_df.empty:
            not_available_df.loc[(not_available_df['author'].str.lower() == author.lower()) &
                                 (not_available_df['title'].str.lower() == title.lower())&
                                 (not_available_df['genre'].str.lower() == genre.lower()) &
                                 (not_available_df['year'] == year),"is_loaned"] ="No"
        not_available_df.to_csv(self.__files[2], index=False)


    def create_books(self,title, author, copies,genre,year):
        """
        in this method we are dealing with creating the new book.

        """
        def normalize_spaces(text):
            return ' '.join(str(text).split())
        if(copies <=0):
            return None
        if genre.lower() not in {genre.lower() for genre in BooksCategory._value2member_map_}:
            print("Genre is not a valid genre")
            return None
        current_year = datetime.now().year
        if not isinstance(year, int)  or -2000>int(year) or int(year)>current_year:
            return None
        title=normalize_spaces(title)
        author=normalize_spaces(author)
        genre=normalize_spaces(genre)
        bookdf=self.create_in_bookscsv(title, author, copies,genre,year)
        book = Books(title, author, "No", copies, genre, year,bookdf['popularity'].values[0])
        self.add_to_available(book)
        self.check_not_available(book)
        if bookdf["copies"].values[0]==copies:
            return True
        return False

