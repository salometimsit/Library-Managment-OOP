class Books:
    l=[]
    def __init__(self, title, author, year, genre, copies):
        self.title = title
        self.author =author
        self.year = year
        self.genre = genre
        self.copies = copies
    def __addbook__(self):
        self.copies += 1
    def __removebook__(self):
        if self.copies!=0:
            self.copies -=1
        else:
            print("No books left to remove")
            self.copies=0;
    def __updatebook__(self):
        self.copies +=1