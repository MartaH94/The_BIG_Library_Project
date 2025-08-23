# loan class with attributes and methods (who borrowed the book, when it was borrowed, when it was returned)

from datetime import datetime
from models.book import Book

class LoanedBook:
    def __init__(self, book : Book, borrowed_by, is_borrowed=False, loan_date=None, return_date=None):
        self.book = book
        self.borrowed_by = borrowed_by
        self.is_borrowed = is_borrowed
        self.loan_date = loan_date or datetime.now()
        self.return_date = return_date

    def borrow_book(self):
        if not self.is_borrowed:
            self.is_borrowed = True
            self.loan_date = datetime.now()
            self.return_date = None
        else:
            raise Exception("Book is already borrowed") # ADD this exception to module exceptions.py and import here

class BookReservation:
    def __init__(self, book : Book, reserved_by, reservation_date=None):
        self.book = book
        self.reserved_by = reserved_by
        self.reservation_date = reservation_date

