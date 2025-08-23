# managing book  operations like: add, edit, search, sort, delete, display

from models.book import Book
import exceptions as exc


class BookService:
    def __init__(self):
        self.books = []

    def add_book(self, book : Book):
        self.books.append(book)
        
    def edit_book(self, book : Book, title=None, author=None, year=None):
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")
        if title:
            book.title = title
        if author:
            book.author = author
        if year:
            book.year = year

    def delete_book(self, book : Book):
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")
        self.books.remove(book)


    def search_books(self, title=None, author=None, year=None):
        results = []
        for book in self.books:
            match = True
            if title and title.lower() not in book.title.lower():
                match = False
            if author and author.lower() not in book.author.lower():
                match = False
            if year and year != book.year:
                match = False
            if match:
                results.append(book)     
        return results

    def get_books_by_category(self, category):
        books_in_category = []
        for book in self.books:
            if category in book.categories:
                books_in_category.append(book)
        return books_in_category


    def is_book_available(self, book : Book):
        if book not in self.books:
            raise exc.BookNotFoundError("Book not found in the library")
        return getattr(book, "is_available", True)

    def get_available_books(self):
        available_books = []
        for book in self.books:
            if getattr(book, "is_available", True):
                available_books.append(book)
        return available_books


    def get_all_books(self):
        return self.books

    def get_all_categories(self):
        categories = set()
        for book in self.books:
            categories.update(book.categories)
        return list(categories)
    

   

    
    


    


    



