class Books:
    #this is a factory class
    def __init__(self, title, author, year, genre, T_copies, Ava_copies):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.T_copies = T_copies
        self.Ava_copies = Ava_copies

    @staticmethod
    def create_book(title, author, year, genre, total_copies):
        return Books(title, author, year, genre, total_copies, total_copies)

    def add_to_library(self):
        self.T_copies += 1
        self.Ava_copies +=1

    def remove_from_library(self):
        if self.T_copies > 0:
            self.T_copies -= 1
            if self.Ava_copies > 0:
                self.Ava_copies-=1
        else:
            print("No copies left to remove.")

    def borrow_book(self):
        if self.Ava_copies > 0:
            self.Ava_copies -= 1
        else:
            print("No available books left to remove")

    def return_book(self):
        if self.Ava_copies < self.T_copies:
            self.Ava_copies += 1
        else:
            print("All copies are in the library.")

    def __str__(self):
        return (f"Title: {self.title}, Author: {self.author}, Year: {self.year}, "f"Genre: {self.genre}, Total Copies: {self.T_copies}, "
                f"Available Copies: {self.Ava_copies}")

