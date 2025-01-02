from Books import Books
class Client:
    __client_id=1111
    def __init__(self, name,):
        self.__name = name
        self.__id = self.__client_id
        self.__books = []
        self.__client_id+=1

    def borrow_book(self, book):
        self.__books.append(book)

    def return_book(self, book):
        self.__books.remove(book)