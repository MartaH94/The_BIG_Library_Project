# book class with atrbutes and methods

class Book:
    def __init__(self, author, title, year):
        self.author = author
        self.title = title
        self.year = year


class BookCategory:
    def __init__(self, name):
        self.name = name
        self.books = []

    def add_book(self, book):
        self.books.append(book)

