import csv
import os

import pandas as pd

from src.main_lib.Books import Books


class Rentals:
    __instance = None

    def __init__(self):
        from src.main_lib.Books import Books
        if Rentals.__instance is None:
            # Path to books.csv inside Excel_Tables under main_lib
            filenames = ['Excel_Tables/books.csv', 'Excel_Tables/available_books.csv',
                         'Excel_Tables/not_available_books.csv']
            self.__files = []
            for filename in filenames:
                # Path to the file inside Excel_Tables under main_lib
                file_path = os.path.join(os.path.dirname(__file__), filename)
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"File not found: {file_path}")

                self.__files.append(file_path)

            self.__books = []
            with open(self.__files[0], mode='r') as b_csv:
                reader = csv.reader(b_csv)
                next(reader, None)
                for row in reader:
                    if len(row) >= 6:
                        self.__books.append(Books(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
                    else:
                        print(f"Invalid row: {row}")

    @staticmethod
    def get_instance():
        if Rentals.__instance is None:
            Rentals.__instance = Rentals()
        return Rentals.__instance

    def rent_books(self, book):
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
                print(f"Book '{book.get_title()}' rented successfully,the remaining copies: {curr - 1}")
            elif curr == 1:
                print(f"you cannot rent the book:'{book.get_title()}', no available books")
                book.set_popularity(book.get_popularity() + 1)
                self.add_to_not_available_csv(book, 1)
                self.remove_from_csv(book, self.__files[1])
        else:
            print(f"you cannot rent the book:'{book.get_title()}', no available books")

    def return_books(self, book):
        b = self.find_in_csv(book, self.__files[2])
        if b is not None:
            curr = int(b['copies'])
            if curr > 0:
                df = pd.read_csv(self.__files[2])
                con = ((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) &
                       (df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year())))
                df.loc[con, 'copies'] = curr - 1
                df.to_csv(self.__files[2], index=False)
                print(f"Book '{book.get_title()}' returned successfully,the remaining copies: {curr - 1}")
            elif curr == 0:
                print(f"you cannot return the book:'{book.get_title()}', no available books")
                self.add_to_available_csv(book, 1)
                self.remove_from_csv(book, self.__files[2])
        else:
            print(f"you cannot rent the book:'{book.get_title()}', no available books")

    def add_to_available_csv(self, book, total_available_copies):
        try:
            if self.find_in_csv(book, self.__files[1]) is None:
                with open(self.__files[1], mode='a', newline='') as av_csv:
                    writer = csv.writer(av_csv)
                    if not os.path.isfile(self.__files[1]) or os.path.getsize(self.__files[1]) == 0:
                        writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity'])
                    writer.writerow(
                        [book.get_title(), book.get_author(), book.get_is_loaned(), total_available_copies,
                         book.get_genre(),
                         book.get_year(), book.get_popularity()])
                print(f"Book '{book.get_title()}' added to available_books successfully.")
            else:
                print(f"Book '{book.get_title()}' already exists in available_books")
        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def add_to_not_available_csv(self, book, total_available_copies):
        try:
            if self.find_in_csv(book, self.__files[2]) is None:
                with open(self.__files[2], mode='a', newline='') as av_csv:
                    writer = csv.writer(av_csv)
                    if not os.path.isfile(self.__files[2]) or os.path.getsize(self.__files[2]) == 0:
                        writer.writerow(['title', 'author', 'is_loaned', 'copies', 'genre', 'year', 'popularity'])
                    writer.writerow(
                        [book.get_title(), book.get_author(), book.get_is_loaned(), total_available_copies,
                         book.get_genre(),
                         book.get_year(), book.get_popularity()])
                print(f"Book '{book.get_title()}' added to not_available_books successfully.")
            else:
                print(f"Book '{book.get_title()}' already exists in not_available_books")
        except Exception as e:
            print(f"An error occurred while adding the book: {e}")

    def find_in_csv(self, book, file):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
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

    # MATCH- used to determine if each string in the underlying data of the given series object matches a regular expression
    def remove_from_csv(self, book, file):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if match.empty:
                print(f"Book '{book.get_title()}' not found in:{file}.csv.")
                return
            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(file, index=False)
            print(f"Book '{book.get_title()}' removed from:{file}.csv.")
            # if not match.empty:
            #     if os.path.isfile(self.__files[2]):
            #         if self.find_in_csv(book, self.__files[2]):
            #             return
            #     match.to_csv(self.__files[2], mode='a', index=False, header=not os.path.isfile(self.__files[2]))
            #     print(f"Book '{book.get_title()}' moved to not_available_books.csv successfully.")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")
    def find_in_csv(self, book, file):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
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


    # MATCH- used to determine if each string in the underlying data of the given series object matches a regular expression
    def remove_from_csv(self, book, file):
        try:
            df = pd.read_csv(file)
            match = df[(df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                       (df['year'].astype(int) == int(book.get_year()))]
            if match.empty:
                print(f"Book '{book.get_title()}' not found in:{file}.csv.")
                return
            df = df[~((df['title'].str.strip().str.lower() == book.get_title().strip().lower()) & (
                    df['author'].str.strip().str.lower() == book.get_author().strip().lower()) &
                      (df['year'].astype(int) == int(book.get_year())))]
            df.to_csv(file, index=False)
            print(f"Book '{book.get_title()}' removed from:{file}.csv.")
            # if not match.empty:
            #     if os.path.isfile(self.__files[2]):
            #         if self.find_in_csv(book, self.__files[2]):
            #             return
            #     match.to_csv(self.__files[2], mode='a', index=False, header=not os.path.isfile(self.__files[2]))
            #     print(f"Book '{book.get_title()}' moved to not_available_books.csv successfully.")
        except FileNotFoundError:
            print(f"File not found: {file}")
        except Exception as e:
            print(f"An error occurred while updating the files: {e}")


if __name__ == '__main__':
    bo = Rentals.get_instance()
    book1 = Books("1984", "George Orwell", "No", 3, "Dystopian", 1949, 0)
    bo.return_books(book1)
