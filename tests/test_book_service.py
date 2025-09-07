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
        print("\n[TEST CASE] test_add_book: Adding new book.")
        self.admin_service.add_book(self.book)
        self.assertIn(self.book, self.admin_service.books)
        print(f"[PASS] test_add_book: Book '{self.book.title}' added succesfully.")
        
    def test_add_book_without_author_or_title(self):
        print("\n[TEST CASE] test add book with empty data (author or title): Adding book with empty author or title... ")
        self.assertRaises(exc.InvalidBookDataError, self.admin_service.add_book, Book(author=None, title=None, year=2020))
        print(f"[PASS] test add book with empty data (author or title): Exception {exc.InvalidBookDataError} raised properly.")   
        
# [TESTS FOR: EDIT BOOK]
    def test_user_has_no_permission_to_edit_book(self):
        print("\nTEST CASE] test_user_has_no_permission_to_edit_book: User role is 'reader', trying to edit book...")
        self.reader_service.books.append(self.book)
        self.assertRaises(exc.PermissionError, self.reader_service.edit_book, self.book, title="New Title")
        print(f"[PASS] test_user_has_no_permission_to_edit_book: Exception {exc.PermissionError} raised properly.")


    def test_edit_books_title(self):
        print("\n[TEST CASE] test_edit_books_title: Adding book and editing its title.") 
        self.admin_service.add_book(self.book)
        self.admin_service.edit_book(self.book, title="Wiersze")
        self.assertEqual(self.book.title, "Wiersze")
        print(f"[PASS] test_edit_book_title: Book title changed to '{self.book.title}' successfully.")

    def test_edit_books_author(self):
        print("\n[TEST CASE] test edit_books_author: Editing books author.")
        self.admin_service.add_book(self.book)
        self.admin_service.edit_book(self.book, author="Juliusz Słowacki")
        self.assertEqual(self.book.author, "Juliusz Słowacki")
        print(f"[PASS] test_edit_book_author: Book author changed to '{self.book.author}' successfully.")

    def test_edit_book_not_found(self):
        print("\n[TEST CASE] test_edit_book_not_found: Trying to edit book which is not present in the library.")
        self.assertRaises(exc.BookNotFoundError, self.admin_service.edit_book, self.book, title="New Title")
        print(f"[PASS] test_edit_book_not_found: Exception {exc.BookNotFoundError} raised properly.")

# [TESTS FOR: DELETE A BOOK]
    def test_delete_book(self):
        print("\n[TEST CASE] test_delete_book: Deleting the book from the library")
        self.admin_service.add_book(self.book)
        self.admin_service.delete_book(self.book)
        print(f"[PASS] test_delete_book: Book '{self.book.title}' by {self.book.author} deleted from the library.")


# [TESTS FOR: SEARCH A BOOK]
    # def test_search_by_author_substring(self):
    #     # This test expects substring matching for author names (e.g., "Mickiewicz" matches "Adam Mickiewicz")
    #     print("\n[TEST CASE] test_search_by_author_substring: Searching book in the full library by partial author name")
    #     self.admin_service.add_book(self.book)
    #     self.reader_service.books = self.admin_service.books
    #     results = self.reader_service.search_books(author="Mickiewicz")
    #     self.assertIsInstance(results, list)
    #     self.assertIn(self.book, results)
    #     print(f"[PASS] test_search_by_author_substring: Searching for a book by partial author name and receiving results successfully.")
    #     print(f"[PASS] test_search_by_author: Book found by author search: '{self.book.title}' by {self.book.author}.")
    #     print(f"[PASS] test_search_by_author: Searching for a book by author and receiving results successfully.")

    def test_search_by_title_or_keyword(self):
        print("\n[TEST CASE] test_search_by_title_or_keyword: Searching for a book by entering the full book title or by keyword")
        self.admin_service.add_book(self.book)
        self.reader_service.books = self.admin_service.books
        results = self.reader_service.search_books(title="Pan")
        self.assertIsInstance(results, list)
        self.assertIn(self.book, results)
        # Also test searching by the full book title
        full_title_results = self.reader_service.search_books(title="Pan Tadeusz")
        self.assertIsInstance(full_title_results, list)
        self.assertIn(self.book, full_title_results)
        print(f"[PASS] test_search_by_title_or_keyword: Book {self.book.title} found and results received successfully")

    def test_search_no_results(self):
        print("\n[TEST CASE] test_search_no_results: No matching books to searched phrase.")
        self.admin_service.add_book(self.book)
        self.reader_service.books = self.admin_service.books
        results = self.reader_service.search_books(match="Whatever")
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 0)
        self.assertRaises(exc.BookNotFoundError, self.reader_service.search_books, title="Whatever")
        print(f"[PASS] test_search_no_results: No matching books found, empty list returned successfully.\nException {exc.BookNotFoundError} raised properly.")






if __name__ == '__main__':
    unittest.main(verbosity=2)