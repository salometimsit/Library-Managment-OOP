from Observer import Observer

class Client(Observer):
    __client_id = 1111

    def __init__(self, name):
        super().__init__()
        self.__name = name
        self.__id = self.__client_id
        self.__books = []
        self.__notification = []
        self.__client_id += 1

    def borrow_book(self, book):
        self.__books.append(book)

    def return_book(self, book):
        self.__books.remove(book)

    def get_books(self):
        return self.__books

    def update(self, subject, message):
        self.__notification.append(message)
