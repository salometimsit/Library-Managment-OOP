import csv
import os
from typing import Tuple
import pandas as pd

from src.main_lib.Books import Books
from src.main_lib.FilesHandle import FilesHandle
from src.main_lib.LibraryServiceLocator import LibraryServiceLocator
from src.main_lib.Logger import Logger
from src.main_lib.Search_Books import SearchBooks


class Rentals:
    """
    Manages the rental system for the library using the Singleton pattern.
    Handles book rentals, returns, and waiting lists.
    """
    __instance = None

    def __init__(self):
        """Initialize the Rentals system"""
        if Rentals.__instance is None:
            self.__initialize_files()
            self.__initialize_books()
            self.__search = SearchBooks().set_strategy("title")
            LibraryServiceLocator.set_rentals(self)

    def __initialize_files(self):
        """Initialize and validate file paths"""
        self.__files = FilesHandle().get_file_by_category("book")
        self.__ensure_waiting_list_column()

    def __ensure_waiting_list_column(self):
        """Ensure waiting_list column exists in not_available_books.csv"""
        df = pd.read_csv(self.__files[2])
        if 'waiting_list' not in df.columns:
            df['waiting_list'] = ''
            df.to_csv(self.__files[2], index=False)

    def __initialize_books(self):
        """Load books from CSV into memory"""
        self.__books = []
        with open(self.__files[0], mode='r') as b_csv:
            reader = csv.reader(b_csv)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 6:
                    self.__books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    @staticmethod
    def get_instance():
        """Get singleton instance"""
        if Rentals.__instance is None:
            Rentals.__instance = Rentals()
        return Rentals.__instance

    def get_library(self):
        """Get library instance"""
        return LibraryServiceLocator.get_library()

    def __create_book_filter(self, book):
        """Create a DataFrame filter for book matching"""
        return lambda df: (
                (df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                (df['year'].astype(int) == int(book.get_year())) &
                (df['genre'].str.strip().str.lower() == book.get_genre().strip().lower())
        )

    def find_in_csv(self, book, file):
        """Find a book in a CSV file"""
        try:
            df = pd.read_csv(file)
            book_filter = self.__create_book_filter(book)
            match = df[book_filter(df)]
            return match.iloc[0].to_dict() if not match.empty else None
        except Exception as e:
            print(f"Error finding book in CSV: {e}")
            return None

    def update_book_status(self, book, file_path, updates):
        """Update book status in CSV file"""
        try:
            df = pd.read_csv(file_path)
            book_filter = self.__create_book_filter(book)

            # Convert updates values to appropriate types
            converted_updates = {}
            for key, value in updates.items():
                if key in ['copies', 'popularity']:
                    converted_updates[key] = int(value)
                else:
                    converted_updates[key] = value

            for key, value in converted_updates.items():
                df.loc[book_filter(df), key] = value

            df.to_csv(file_path, index=False)
            return True
        except Exception as e:
            print(f"Error updating book status: {e}")
            return False

    def add_to_waiting_list(self, book: Books, name: str, phone: str,email: str) -> bool:
        """Add person to book's waiting list"""
        df = pd.read_csv(self.__files[2])
        df['waiting_list'] = df['waiting_list'].astype(str)
        book_filter = self.__create_book_filter(book)
        if not book_filter(df).any():
            return False

        current_list = df.loc[book_filter(df), 'waiting_list'].iloc[0]
        new_entry = f"{name}:{phone}:{email}"

        if pd.isna(current_list) or current_list == 'nan' or current_list == '' or current_list == '[]':
            df.loc[book_filter(df), 'waiting_list'] = new_entry
            df.to_csv(self.__files[2], index=False)
            return True

        waiting_list = current_list.split(';')

        # Check for existing entry
        for entry in waiting_list:
            if ':' in entry:
                entry_name, entry_phone, entry_email = entry.split(':')
                if entry_name.strip().lower() == name.strip().lower() and (entry_phone.strip() == phone.strip() or
                        entry_email.strip() == email.strip()):
                    return False

        if len(waiting_list) >= 10:
            return False

        df.loc[book_filter(df), 'waiting_list'] = f"{current_list};{new_entry}"
        df.to_csv(self.__files[2], index=False)
        return True

    def check_waiting_list(self, book: Books) -> Tuple[str, str, str]:
        """Get and remove first person from waiting list"""
        df = pd.read_csv(self.__files[2])
        book_filter = self.__create_book_filter(book)

        if not book_filter(df).any():
            return None, None, None

        waiting_list = df.loc[book_filter(df), 'waiting_list'].iloc[0]
        if pd.isna(waiting_list) or waiting_list == '' or waiting_list == '[]':
            return None, None, None

        entries = waiting_list.split(';')
        if not entries:
            return None, None, None

        first_person = entries[0]
        if ':' not in first_person:
            return None, None, None

        name, phone ,email= first_person.split(':')
        self.update_book_status(book, self.__files[2],
                                {'waiting_list': ';'.join(entries[1:])})
        return name.strip(), phone.strip() ,email.strip()

    @Logger.log_method_call("Book borrowed")
    def rent_books(self, book):
        """Rent a book to a client"""
        available_book = self.find_in_csv(book, self.__files[1])
        if not available_book:
            self.add_popularity(book)
            return False

        curr_copies = int(available_book['copies'])
        if curr_copies > 1:
            self.update_book_status(book, self.__files[1], {'copies': curr_copies - 1})
            self.__handle_not_available_copy(book)
        else:
            self.__handle_last_available_copy(book)
        return True

    @Logger.log_method_call("Book returned")
    def __process_book_return(self, book, not_available_book):
        curr_copies = int(not_available_book['copies'])
        if curr_copies > 1:
            self.__handle_multiple_copy_return(book, curr_copies)
        else:
            self.__handle_single_copy_return(book)
        return True

    def return_books(self, book):
        not_available_book = self.find_in_csv(book, self.__files[2])
        if not not_available_book:
            return False

        # שמירת רשימת ההמתנה המקורית
        waiting_list = not_available_book.get('waiting_list', '')
        if pd.isna(waiting_list):
            waiting_list = ''

        # יצירת רשימת ההמתנה המעודכנת (ללא האדם הראשון)
        updated_waiting_list = ''
        if waiting_list and waiting_list.strip():
            entries = waiting_list.split(';')
            if len(entries) > 1:
                updated_waiting_list = ';'.join(entries[1:])

        # בדיקה אם יש מישהו ברשימת המתנה
        name, phone , email= self.check_waiting_list(book)

        # ביצוע ההחזרה
        return_success = self.__process_book_return(book, not_available_book)
        if not return_success:
            return False

        # אם יש מישהו ברשימת המתנה
        if name and phone:
            msg = (f"The Book '{book.get_title()}' has been returned and should be transferred to {name},\n"
                   f" Phone: {phone} \n Email: {email}")
            self.get_library().notify(msg)
            # השאלת הספר למי שממתין
            self.rent_books(book)
            # עדכון רשימת ההמתנה לרשימה ללא האדם הראשון
            self.update_book_status(book, self.__files[2], {'waiting_list': updated_waiting_list})

        return True

    def add_popularity(self, book):
        """Increase book popularity across all files"""
        for file_path in self.__files:
            book_entry = self.find_in_csv(book, file_path)
            if book_entry:
                current_popularity = int(book_entry['popularity'])
                self.update_book_status(book, file_path, {'popularity': current_popularity + 1})

    def __handle_not_available_copy(self, book):
        """Handle adding a copy to not available books"""
        not_available = self.find_in_csv(book, self.__files[2])
        if not_available:
            curr = int(not_available['copies'])
            self.update_book_status(book, self.__files[2], {'copies': curr + 1})
        else:
            self.__add_to_not_available_csv(book, 1)

    def __handle_last_available_copy(self, book):
        """Handle renting the last available copy"""
        not_available = self.find_in_csv(book, self.__files[2])
        if not_available:
            curr = int(not_available['copies'])
            self.update_book_status(book, self.__files[2],
                                    {'copies': curr + 1, 'is_loaned': 'No'})
            self.update_book_status(book, self.__files[0], {'is_loaned': 'No'})
        else:
            self.__add_to_not_available_csv(book, 1)
        self.__remove_from_csv(book, self.__files[1])

    def __handle_multiple_copy_return(self, book, curr_copies):
        """Handle returning one of multiple copies"""
        self.update_book_status(book, self.__files[2], {'copies': curr_copies - 1})
        available = self.find_in_csv(book, self.__files[1])
        if available:
            curr = int(available['copies'])
            self.update_book_status(book, self.__files[1], {'copies': curr + 1})
        else:
            self.__add_to_available_csv(book, 1)

    def __handle_single_copy_return(self, book):
        """Handle returning the last copy"""
        self.update_book_status(book, self.__files[2],
                                {'copies': 1, 'is_loaned': 'No'})
        self.update_book_status(book, self.__files[0], {'is_loaned': 'No'})
        self.__add_to_available_csv(book, book.get_total_books())
        self.__remove_from_csv(book, self.__files[2])

    def __add_to_available_csv(self, book, copies):
        """Add book to available books CSV"""
        if self.find_in_csv(book, self.__files[1]) is None:
            with open(self.__files[1], mode='a', newline='') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.__files[1]) == 0:
                    writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity'])
                writer.writerow([
                    book.get_title(), book.get_author(), "No", copies,
                    book.get_genre(), book.get_year(), book.get_popularity()
                ])

    def __add_to_not_available_csv(self, book, copies):
        """Add book to not available books CSV"""
        if self.find_in_csv(book, self.__files[2]) is None:
            with open(self.__files[2], mode='a', newline='') as f:
                writer = csv.writer(f)
                if os.path.getsize(self.__files[2]) == 0:
                    writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity',
                                     'waiting_list'])
                writer.writerow([
                    book.get_title(), book.get_author(), book.get_is_loaned(), copies,
                    book.get_genre(), book.get_year(), book.get_popularity(), ''
                ])

    def __remove_from_csv(self, book, file):
        """Remove book from CSV file"""
        try:
            df = pd.read_csv(file)
            book_filter = self.__create_book_filter(book)
            df = df[~book_filter(df)]
            df.to_csv(file, index=False)
        except Exception as e:
            print(f"Error removing book from CSV: {e}")
