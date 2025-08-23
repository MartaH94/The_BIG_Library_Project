# book class with atrbutes and methods

class Book:
    def __init__(self, author, title, year, is_borrowed=False, borrowed_by=None):
        self.author = author
        self.title = title
        self.year = year
        self.is_borrowed = is_borrowed
        self.borrowed_by = borrowed_by

class BookCategory:
    def __init__(self, name):
        self.name = name
        self.books = []
        
    def add_book(self, book):
        self.books.append(book)

