class Books:
    def __init__(self, title, author, year, genre, T_copies,Ava_copies):
        self.title = title
        self.author =author
        self.year = year
        self.genre = genre
        self.T_copies = T_copies
        self.Ava_copies = Ava_copies
    def borrow_book(self):
        if self.Ava_copies != 0:
            self.Ava_copies -=1
        else:
            print("No availible books left to remove")
            self.Ava_copies=0
    def return_book(self):
        self.Ava_copies +=1