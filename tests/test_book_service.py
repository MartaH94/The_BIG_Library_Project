# file for unit tests: book service and book handling

# This is not a full list of Testcases to test yet. 


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

        self.book_service = BookService(self.admin_authorisation)
        self.book_service.books = []
        self.book_service.books.append(Book(author="J.K. Rowling", title="Harry Potter and the Philosopher's Stone", year=1997))
        self.book_service.books.append(Book(author="George Orwell", title="1984", year=1949))
        self.book_service.books.append(Book(author="J.R.R. Tolkien", title="The Hobbit", year=1937))
        self.book_service.books.append(Book(author="F. Scott Fitzgerald", title="The Great Gatsby", year=1925))

        self.book = Book(author="Sample Author", title="Sample Title 2020", year=2020)

        self.admin_service.books = self.book_service.books.copy()
        self.reader_service.books = self.book_service.books.copy()

# [TESTS FOR: ADDING BOOK]        
    def test_add_book(self):
        print("\n[TEST CASE FOR: ADDING BOOK] test_add_book: Adding new book.")
        book_to_add = self.book_service.books[0]
        self.admin_service.add_book(book_to_add)
        self.assertIn(book_to_add, self.admin_service.books)
        print(f"[PASS] test_add_book: Book '{book_to_add.title}' added succesfully.")
        
    def test_add_book_without_author_or_title(self):
        print("\n[TEST CASE FOR: ADDING BOOK] add book with empty data (author or title): Adding book with empty author or title... ")
        self.assertRaises(exc.InvalidBookDataError, self.admin_service.add_book, Book(author=None, title=None, year=2020))
        print(f"[PASS] test add book with empty data (author or title): Exception {exc.InvalidBookDataError} raised properly.")   
        
# [TESTS FOR: EDIT BOOK]
    def test_user_has_no_permission_to_edit_book(self):
        print("\nTEST CASE FOR: EDIT BOOK] user_has_no_permission_to_edit_book: User role is 'reader', trying to edit book...")
        book_to_edit = self.book_service.books[1]
        self.assertRaises(exc.PermissionError, self.reader_service.edit_book, book_to_edit, title="New Title")
        print(f"[PASS] test_user_has_no_permission_to_edit_book: Exception {exc.PermissionError} raised properly.")

    def test_edit_books_title(self):
        print("\n[TEST CASE FOR: EDIT BOOK] test_edit_books_title: Adding book and editing its title.") 
        book_to_edit = self.book_service.books[1]
        self.admin_service.edit_book(book_to_edit, title="Title Edited")
        self.assertEqual(book_to_edit.title, "Title Edited")
        print(f"[PASS] test_edit_book_title: Book title changed to '{book_to_edit.title}' successfully.")

    def test_edit_books_author(self):
        print("\n[TEST CASE FOR: EDIT BOOK] edit_books_author: Editing books author.")
        book_to_edit = self.book_service.books[1]
        self.admin_service.edit_book(book_to_edit, author="Edited Author")
        self.assertEqual(book_to_edit.author, "Edited Author")
        print(f"[PASS] test_edit_book_author: Book author changed to '{book_to_edit.author}' successfully.")

    def test_edit_books_year(self):
        print("\n[TEST CASE FOR: EDIT BOOK: test_edit_book_year: Edition of the book year]")

    def test_edit_book_not_found(self):
        print("\n[TEST CASE FOR: EDIT BOOK] edit_book_not_found: Trying to edit book which is not present in the library.")
        self.book = Book(author="Adam Mickiewicz", title="Pan Tadeusz", year=1834)
        self.assertRaises(exc.BookNotFoundError, self.admin_service.edit_book, self.book, title="New Title")
        print(f"[PASS] test_edit_book_not_found: Exception {exc.BookNotFoundError} raised properly.")


# [TESTS FOR: DELETE A BOOK]
    def test_delete_book(self):
        print("\n[TEST CASE FOR: DELETE A BOOK] delete_book: Deleting the book from the library")
        book_to_delete = self.book_service.books[2]
        self.admin_service.delete_book(book_to_delete)
        print(f"[PASS] test_delete_book: Book '{book_to_delete.title}' by {book_to_delete.author} deleted from the library.")


# [TESTS FOR: SEARCH A BOOK]
    def test_search_by_keyword(self):
        print("\n[TEST CASE FOR: SEARCH A BOOK] search_by_keyword: Search book by title, author or year")
        book_to_find = self.book_service.books[0]
        search_phrase = self.reader_service.search_books(searched_term="Harry")
        self.assertIsInstance(search_phrase, list)
        self.assertIn(book_to_find, search_phrase)
        print(f"[PASS] The book {book_to_find.title} by {book_to_find.author} has been found.")

    def test_no_search_results(self):
        print("\n[TEST CASE FOR: SEARCH A BOOK] no_search_result: No result for searching phrase while user's searching.")
        search_phrase  = self.reader_service.search_books(searched_term="Whatever")
        self.assertIsInstance(search_phrase, list)
        self.assertEqual(len(search_phrase), 0)
        print("[PASS] No book found, returning an empty list.")




if __name__ == '__main__':
    unittest.main(verbosity=2)