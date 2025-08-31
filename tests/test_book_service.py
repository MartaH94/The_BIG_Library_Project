# file for unit tests: book service and book handling
import unittest
from models.book import Book
from models.user import User
from services.book_service import BookService
from services.authorisation_service import UserAuthorisation
import exceptions as exc

class TestBookService(unittest.TestCase):

    def setUp(self):
        self.admin_user = User(user_id="Marta",email="test@test.com", role="admin")
        self.reader_user = User(user_id="John", email="john@test.com", role="reader")

        self.admin_authorisation = UserAuthorisation()
        self.admin_authorisation.login(self.admin_user)

        self.reader_authorisation = UserAuthorisation()
        self.reader_authorisation.login(self.reader_user)

        self.admin_service = BookService(self.admin_authorisation)
        self.reader_service = BookService(self.reader_authorisation)

        self.book = Book(author="Adam Mickiewicz", title="Pan Tadeusz", year=1834)
        print("\n[SETUP] Creating users and BookService instances for this test.")



# [TESTS FOR: ADDING BOOK]       
 
    def test_add_book(self):
        print("[TEST CASE] test_add_book: Adding new book.")
        self.admin_service.add_book(self.book)
        self.assertIn(self.book, self.admin_service.books)
        print(f"\n[PASS] test_add_book: Book '{self.book.title}' added succesfully.")
        
    def test_add_book_without_author_or_title(self):
        print("[TEST CASE] test add book with empty data (author or title): Adding book with empty author or title... ")
        self.assertRaises(exc.InvalidBookDataError, self.admin_service.add_book, Book(author=None, title=None, year=2020))
        print(f"\n[PASS] test add book with empty data (author or title): Exception {exc.InvalidBookDataError} raised properly.")   
        
# [TESTS FOR: EDIT BOOK]
    def test_user_has_no_permission_to_edit_book(self):
        print("TEST CASE] test_user_has_no_permission_to_edit_book: User role is 'reader', trying to edit book...")
        self.reader_service.books.append(self.book)
        self.assertRaises(exc.PermissionError, self.reader_service.edit_book, self.book, title="New Title")
        print(f"\n[PASS] test_user_has_no_permission_to_edit_book: Exception {exc.PermissionError} raised properly.")


    def test_edit_books_title(self):
        print("[TEST CASE] test_edit_books_title: Adding book and editing its title.") 
        self.admin_service.add_book(self.book)
        self.admin_service.edit_book(self.book, title="Wiersze")
        self.assertEqual(self.book.title, "Wiersze")
        print(f"\n[PASS] test_edit_book_title: Book title changed to '{self.book.title}' successfully.")

    def test_edit_books_author(self):
        print("[TEST CASE] test edit_books_author: Editing books author.")
        self.admin_service.add_book(self.book)
        self.admin_service.edit_book(self.book, author="Juliusz Słowacki")
        self.assertEqual(self.book.author, "Juliusz Słowacki")
        print(f"[PASS] test_edit_book_author: Book author changed to '{self.book.author}' successfully.")
    

if __name__ == '__main__':
    unittest.main(verbosity=2)