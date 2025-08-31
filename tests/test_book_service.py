# file for unit tests: book service and book handling
import unittest
from models.book import Book
from models.user import User
from services.book_service import BookService
from services.authorisation_service import UserAuthorisation
import exceptions as exc

class TestBookService(unittest.TestCase):

    def setUp(self):
        self.user = User(user_id="Marta",email="test@test.com", role="admin")
        self.authorisation = UserAuthorisation()
        self.authorisation.login(self.user)
        self.service = BookService(self.authorisation)
        self.book = Book(author="Adam Mickiewicz", title="Pan Tadeusz", year=1834)
        print("\n[SETUP] Utworzono użytkownika, autoryzację i instancję BookService.")
        
    def test_add_book(self):
        print("[TEST] test_add_book: Dodaję książkę...")
        self.service.add_book(self.book)
        self.assertIn(self.book, self.service.books)
        print(f"[PASS] test_add_book: Książka '{self.book.title}' została dodana pomyślnie.")
        
    def test_add_book_without_author_or_title(self):
        print("[TEST] test add book with empty data (author or title): \nAdding book with empty author or title... ")
        self.assertRaises(exc.InvalidBookDataError, self.service.add_book, Book(author=None, title=None, year=2020))
        print(f"[PASS] test add book with empty data (author or title): \nException {exc.InvalidBookDataError} raised properly.")   
        

    def test_edit_book(self):
        print("[TEST] test_edit_book: Dodaję książkę i edytuję tytuł...") 
        self.service.add_book(self.book)
        self.service.edit_book(self.book, title="Wiersze")
        self.assertEqual(self.book.title, "Wiersze")
        print(f"[PASS] test_edit_book: Tytuł książki został zmieniony na '{self.book.title}' pomyślnie.")

    

if __name__ == '__main__':
    unittest.main(verbosity=2)