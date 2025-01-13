import csv
import os
from typing import Tuple
import pandas as pd

from src.main_lib.BookIterator import BookIterator
from src.main_lib.Books import Books
from src.main_lib.Logger import Logger
from src.main_lib.Search_Books import SearchBooks


class Rentals:
    """
    Represents the rental management system for the library.
    Implements the Singleton pattern.

    Attributes:
        __instance (Rentals): Singleton instance of the Rentals class.
        __files (list): List of file paths for books, available_books, and not_available_books CSV files.
        __books (list): List of books managed for rentals.
    """
    global popularlist
    __instance = None

    def __init__(self):
        """
        Initializes the Rentals instance and loads book data from CSV files.
        """
        if Rentals.__instance is None:
            # Initialize file paths
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv']
            self.__files = []
            for filename in filenames:
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.__files.append(file_path)

            # Add waiting_list column to not_available_books.csv if it doesn't exist
            not_available_df = pd.read_csv(self.__files[2])
            if 'waiting_list' not in not_available_df.columns:
                not_available_df['waiting_list'] = ''
                not_available_df.to_csv(self.__files[2], index=False)

            self.__books = []
            with open(self.__files[0], mode='r') as b_csv:
                reader = csv.reader(b_csv)
                next(reader, None)  # Skip header
                for row in reader:
                    if len(row) >= 6:
                        self.__books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    else:
                        print(f"Invalid row: {row}")
            self.__search = SearchBooks().set_strategy("title")

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of the Rentals class.

        Returns:
            Rentals: Singleton instance of the Rentals.
        """
        if Rentals.__instance is None:
            Rentals.__instance = Rentals()
        return Rentals.__instance

    def change_loaned_book(self, book, status):
        c = self.find_in_csv(book, self.__files[0])
        if c is not None:
            df = pd.read_csv(self.__files[0])
            con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                   (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year())))

            df.loc[con, 'is_loaned'] = status
            df.to_csv(self.__files[0], index=False)
            print("changed loaned status")
        else:
            print("no value found")

    def change_popularity_inbook(self, book, status):
        c = self.find_in_csv(book, self.__files[0])
        if c is not None:
            df = pd.read_csv(self.__files[0])
            con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                   (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year())))

            df.loc[con, 'popularity'] = status
            df.to_csv(self.__files[0], index=False)
            print("changed popularity status")
        else:
            print("no value found")

    def add_to_waiting_list(self, book: Books, name: str, phone: str) -> bool:
        """
        Adds a person to the waiting list for a book if they're not already in the list
        and if the list hasn't reached its maximum capacity of 10 people.

        Args:
            book (Books): The book to add to waiting list
            name (str): Name of the person
            phone (str): Phone number of the person

        Returns:
            bool: True if successfully added, False otherwise
        """
        df = pd.read_csv(self.__files[2])
        con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
               (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
               (df['year'].astype(int) == int(book.get_year())))

        if con.any():
            current_list = df.loc[con, 'waiting_list'].iloc[0]
            new_entry = f"{name}:{phone}"

            # Check if list is empty or contains invalid data
            if pd.isna(current_list) or current_list == '' or current_list == '[]':
                df.loc[con, 'waiting_list'] = new_entry
                df.to_csv(self.__files[2], index=False)
                print(f"Added {name} to waiting list for '{book.get_title()}'")
                return True

            # Convert current list to array of entries
            waiting_list = current_list.split(';')

            # Check if person is already in list
            for entry in waiting_list:
                # Check if entry is in valid format "name:phone"
                if ':' in entry:
                    entry_name, entry_phone = entry.split(':')
                    if entry_name.strip().lower() == name.strip().lower() and entry_phone.strip() == phone.strip():
                        print(f"{name} is already in the waiting list for '{book.get_title()}'")
                        return False
                else:
                    print(f"Invalid entry format in waiting list: '{entry}'")

            # Check if list has reached maximum capacity
            if len(waiting_list) >= 10:
                print(f"Waiting list for '{book.get_title()}' is full (maximum 10 people)")
                return False

            # Add new entry to list
            df.loc[con, 'waiting_list'] = f"{current_list};{new_entry}"
            df.to_csv(self.__files[2], index=False)
            print(f"Added {name} to waiting list for '{book.get_title()}'")
            return True

        return False

    def check_waiting_list(self, book: Books) -> Tuple[str, str]:
        """
        Checks if there are people in the waiting list and returns the first person.

        Args:
            book (Books): The book to check

        Returns:
            Tuple[str, str]: (name, phone) of first person in waiting list, or (None, None) if empty
        """
        df = pd.read_csv(self.__files[2])
        con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
               (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
               (df['year'].astype(int) == int(book.get_year())))

        if con.any():
            waiting_list = df.loc[con, 'waiting_list'].iloc[0]

            # Check if the waiting list is empty or contains invalid data
            if pd.notna(waiting_list) and waiting_list != '' and waiting_list != '[]':
                entries = waiting_list.split(';')
                if len(entries) > 0:
                    first_person = entries[0]

                    # Check if the first entry is in the correct format
                    if ':' in first_person:
                        name, phone = first_person.split(':')
                        # Remove first person from list
                        remaining_list = ';'.join(entries[1:])
                        df.loc[con, 'waiting_list'] = remaining_list
                        df.to_csv(self.__files[2], index=False)

                        return name.strip(), phone.strip()
                    else:
                        print(f"Invalid format for entry '{first_person}'. Skipping.")
                        return None, None
            else:
                print("Waiting list is empty or contains invalid data.")
                return None, None

        return None, None

    def rent_books(self, book):
        """
        Rents a book to a client by decrementing the available copies.

        Args:
            book (Books): Book to be rented.
        """
        b = self.find_in_csv(book, self.__files[1])
        if b is not None:
            curr = int(b['copies'])
            if curr > 1:
                df = pd.read_csv(self.__files[1])
                con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year())))
                df.loc[con, 'copies'] = curr - 1
                df.to_csv(self.__files[1], index=False)
                print(f"Book '{book.get_title()}' rented successfully, remaining copies: {curr - 1}")
                c = self.find_in_csv(book, self.__files[2])
                if c is not None:
                    curr = int(c['copies'])
                    df = pd.read_csv(self.__files[2])
                    con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                           (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                           (df['year'].astype(int) == int(book.get_year())))
                    df.loc[con, 'copies'] = curr + 1
                    df.to_csv(self.__files[2], index=False)
                    return True
                else:
                    self.add_to_not_available_csv(book, 1)
                    return True
            elif curr == 1:
                c = self.find_in_csv(book, self.__files[2])
                if c is not None:
                    curr = int(c['copies'])
                    df = pd.read_csv(self.__files[2])
                    con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                           (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                           (df['year'].astype(int) == int(book.get_year())))
                    df.loc[con, 'copies'] = curr + 1
                    df.loc[con, 'is_loaned'] = "No"
                    df.to_csv(self.__files[2], index=False)
                    self.change_loaned_book(book, "No")
                else:
                    self.add_to_not_available_csv(book, 1)
                self.remove_from_csv(book, self.__files[1])
        else:
            print(f"You cannot rent the book '{book.get_title()}', no available copies.")
            self.add_popularity(book)
            return False
        return True

    def add_popularity(self, book):
        """
        Increases the popularity of a book by 1 in all three CSV files.

        Args:
            book (Books): The book to update popularity for.
        """
        # Update popularity in main books file
        book_entry = self.find_in_csv(book, self.__files[0])
        if book_entry is not None:
            df = pd.read_csv(self.__files[0])
            con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                   (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year())))
            current_popularity = int(book_entry['popularity'])
            df.loc[con, 'popularity'] = current_popularity + 1
            df.to_csv(self.__files[0], index=False)

        # Update popularity in available books file
        available_entry = self.find_in_csv(book, self.__files[1])
        if available_entry is not None:
            df = pd.read_csv(self.__files[1])
            con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                   (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year())))
            current_popularity = int(available_entry['popularity'])
            df.loc[con, 'popularity'] = current_popularity + 1
            df.to_csv(self.__files[1], index=False)

        # Update popularity in not available books file
        not_available_entry = self.find_in_csv(book, self.__files[2])
        if not_available_entry is not None:
            df = pd.read_csv(self.__files[2])
            con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                   (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                   (df['year'].astype(int) == int(book.get_year())))
            current_popularity = int(not_available_entry['popularity'])
            df.loc[con, 'popularity'] = current_popularity + 1
            df.to_csv(self.__files[2], index=False)

        print("Updated popularity in all files successfully")

    def return_books(self, book):
        """
        Returns a rented book by incrementing the available copies.

        Args:
            book (Books): Book to be returned.
        """
        b = self.find_in_csv(book, self.__files[2])
        if b is not None:
            # Check waiting list first
            name, phone = self.check_waiting_list(book)
            if name and phone:
                print(f"Book '{book.get_title()}' has been assigned to {name} ({phone}) from the waiting list")
                return name  # Return the name of the person who gets the book

            curr = int(b['copies'])
            if curr > 1:
                df = pd.read_csv(self.__files[2])
                con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year())))
                df.loc[con, 'copies'] = curr - 1
                df.to_csv(self.__files[2], index=False)
                print(f"Book '{book.get_title()}' returned successfully, remaining copies: {curr + 1}")
                c = self.find_in_csv(book, self.__files[1])
                if c is not None:
                    curr = int(c['copies'])
                    df = pd.read_csv(self.__files[1])
                    con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                           (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                           (df['year'].astype(int) == int(book.get_year())))
                    df.loc[con, 'copies'] = curr + 1
                    df.to_csv(self.__files[1], index=False)
                else:
                    self.add_to_available_csv(book, 1)
            elif curr == 1:
                c = self.find_in_csv(book, self.__files[2])
                if c is not None:
                    curr = int(c['copies'])
                    df = pd.read_csv(self.__files[2])
                    con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                           (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                           (df['year'].astype(int) == int(book.get_year())))
                    df.loc[con, 'copies'] = curr + 1
                    df.loc[con, 'is_loaned'] = "No"
                    df.to_csv(self.__files[2], index=False)
                    self.change_in_book(book, "No")
                self.add_to_available_csv(book, book.get_total_books())
                self.remove_from_csv(book, self.__files[2])
        else:
            print(f"You cannot return the book '{book.get_title()}', no loaned copies.")
            return False
        return True

    def add_to_available_csv(self, book, total_available_copies):
        """
        Adds a book to the available books CSV file.

        Args:
            book (Books): Book to be added.
            total_available_copies (int): Number of copies to add.
        """
        try:
            if self.find_in_csv(book, self.__files[1]) is None:
                with open(self.__files[1], mode='a', newline='') as av_csv:
                    writer = csv.writer(av_csv)
                    if not os.path.isfile(self.__files[1]) or os.path.getsize(self.__files[1]) == 0:
                        writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity'])
                    writer.writerow(
                        [book.get_title(), book.get_author(), "No", total_available_copies,
                         book.get_genre(), book.get_year(), book.get_popularity()])
                print(f"Book '{book.get_title()}' added to available_books successfully.")
            else:
                print(f"Book '{book.get_title()}' already exists in available_books.")
        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def add_to_not_available_csv(self, book, total_available_copies):
        """
        Adds a book to the not available books CSV file.

        Args:
            book (Books): Book to be added.
            total_available_copies (int): Number of copies to add.
        """
        try:
            if self.find_in_csv(book, self.__files[2]) is None:
                with open(self.__files[2], mode='a', newline='') as av_csv:
                    writer = csv.writer(av_csv)
                    if not os.path.isfile(self.__files[2]) or os.path.getsize(self.__files[2]) == 0:
                        writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity',
                                         'waiting_list'])
                    writer.writerow(
                        [book.get_title(), book.get_author(), book.get_is_loaned(), total_available_copies,
                         book.get_genre(), book.get_year(), book.get_popularity(), ''])
                print(f"Book '{book.get_title()}' added to not_available_books successfully.")
            else:
                print(f"Book '{book.get_title()}' already exists in not_available_books.")
        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def find_in_csv(self, book, file):
        """
        Finds a book in the specified CSV file.

        Args:
            book (Books): Book to find.
            file (str): Path to the CSV file.

        Returns:
            dict: A dictionary of the book details if found, else None.
        """
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if not match.empty:
                return match.iloc[0].to_dict()
            else:
                return None
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"An error occurred in find_in_csv: {e}")
            return None

    def remove_from_csv(self, book, file):
        """
        Removes a book from the specified CSV file.

        Args:
            book (Books): Book to remove.
            file (str): Path to the CSV file.
        """
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if match.empty:
                print(f"Book '{book.get_title()}' not found in {file}.")
            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                      (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(file, index=False)
            print(f"Book '{book.get_title()}' removed from {file}.")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")


if __name__ == '__main__':
    rentals = Rentals.get_instance()
    book1 = Books("The Great Gatsby", "F. Scott Fitzgerald", "No", 2, "Fiction", 1925, 0)

    # Example of trying to rent a book and adding to waiting list if unavailable
    if not rentals.rent_books(book1):
        rentals.add_to_waiting_list(book1, "John Doe", "123-456-7890")

    # Example of returning a book and checking waiting list
    result = rentals.return_books(book1)
    if isinstance(result, str):
        print(f"Book automatically assigned to {result} from waiting list")
