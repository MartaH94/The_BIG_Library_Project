"""
________________________________________________________
database.book_json_file_service
========================================================
Service class for managing book data in a JSON file.
________________________________________________________

TO DO HERE:
- Verify implemented methods.
- Implement new methods. Verify what is needed. 
- verify imports 
- Add permissions! 

- methods to add: get book data, get all books list, update book record id, update file data, delete book by matching parameters, maybe sth else.


"""

import json
import utils.config as config
import exceptions as exc

from utils.config import THE_LIBRARY_FILE_PATH
from database.json_files_major_services import JsonFilesService
from services.authorisation_service import UserAuthorisation

class BookJsonFileService():
    """Service class for managing book data in a JSON file. This class provides methods to retrive data of specific book, get book of all available books, update data of book, delete book with matching parameter.
    
    Note for future me: In GUI user will choose books from list to delete. 

    """
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=THE_LIBRARY_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def get_book_data(self, book_id):
        """I search for book data here by id. I also need searching by keyword. 

        Args:
            book_id (_type_): _description_
        """
        current_data = self.json_service.load_json_file()
        book_found = False
        book_data = None

        for book in current_data:
            if book["id"] == book_id:
                book_data = book
                book_found = True

        if not book_found:
            raise exc.BookNotFoundError(f"Book with {book_id} does not exists in database.")
        
        return book_data
        

    def get_all_books_list(self, book_id):
        current_data = self.json_service.load_json_file()
        all_books = []
        book_found = False

        for book in current_data:
            if book["book_id"] == book_id:
                try:
                    all_books.append(book)
                    book_found = True
                except KeyError:
                    raise exc.BookNotFoundError(f"Book with ID {book_id} does not exists in database.")
            if not book_found:
                raise exc.BookError(f"No book in database. Impossible to add book with ID: {book["book_id"]} to all books list.")
        return all_books


    def update_book_data(self):
        pass

    def delete_book_from_database(self):
        pass












    def update_file_data(self, book_id, field, new_value):
        """
        This method is a base for planned new methods. look on top docstring
        
        :param self: Description
        :param book_id: Description
        :param field: Description
        :param new_value: Description
        """
        self.authorisation.check_permission("edit_book")
        self.json_service.file_exists_checkout()
        current_data = self.json_service.read_json_file()

        if not new_value:
            return "I want to put information to user that he should add the value to change or he can cancel this action. It will be presented in GUI."

        book_found = False
        for book in current_data:
            if book["id"] == book_id:
                try:
                    book[field] = new_value
                    book_found = True
                except KeyError:
                    raise exc.InvalidFieldError(f"Field {field} does not exists in library file.")

        if not book_found:
            raise exc.BookNotFoundError(f"Book with {book_id} not found in the library.")
        
        self.json_service.write_json_data(current_data)
        return "PLACEHOLDER: Here there will be confirmation for user that change have been done successfuly, using GUI"

    
    def delete_data_from_file(self, book_id):
        """
        This method is a base for planned new methods. look on top docstring
        
        :param self: Description
        :param book_id: Description
        """
        self.authorisation.check_permission("delete_book")
        self.json_service.file_exists_checkout()
        current_data = self.json_service.read_json_file()

        if not book_id:
            raise exc.BookValidationError(f"Book_id can not be empty field.")

        book_found = False
        for book in current_data:
            if book["id"] == book_id:
                current_data.remove(book)
                book_found = True

        if not book_found:
            raise exc.BookNotFoundError("Book not found in the library. Nothing to delete from library.")
        
        self.json_service.write_json_data(current_data)
        return "Placeholder for delete confirmation to user, using GUI"