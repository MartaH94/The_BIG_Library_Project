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
- Check code of get_book_data method if it's sufficient and correct.

Delete permission checks in all methods. <-- Checking permissions will go to functionality.

methods added: get book data, get all books list, update book data, delete book by id
methods that can be added: 





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

    def add_book_data(self, book_data):
        """ Adds data of new book to database file. Validates book_data against schema. Checks uniqueness of ID.

        Guidelines:
        - book_data must be dictionary
        - load the file
        - checking id uniqueness - check if you can use existing method
        - verify book data (check if all fields are correct; author, title, year, etc)
        - Add the book_data to database 
        - Save the changes


        Args:
            book_data (_type_): _description_
        """
        current_data = self.json_service.load_json_file()
        validated_book_data = self.json_service.validate_against_schema(book_data)
        book_id = book_data["book_id"]

        if not book_data:
            raise exc.DataError("Book data to save is missing or it's incorrect.")
        
        if not isinstance(book_data, dict):
            raise exc.DataTypeError("Book data type is incorrect. Book data must be a dict type.")
        
        for book in current_data:
            if book["book_id"] == book_id:
                raise exc.BookError(f"Book with ID: {book["book_id"]} exists in the database. ID number must be unique value.")
            
        if not validated_book_data:
            raise exc.BookValidationError("Validation failed. Book data doesn't match database file schema.")
        else:
            current_data.append(book_data)

        self.json_service.write_json_data(current_data)

        return "New book record added to the database without errors."



    def get_book_data(self, book_id):
        """ Searching for the book in the library by book ID. This method wilb be used in library for instance before book loan or before chanching thr book's status.

        Returned book_data ought to be a dictionary! 

        Args:
            book_id (str): Unique ID of the book.
        """
        current_data = self.json_service.load_json_file()
        book_found = False
        book_data = None

        for book in current_data:
            if book["book_id"] == book_id:
                book_data = book
                book_found = True

        if not book_found:
            raise exc.BookNotFoundError(f"Book with {book_id} does not exists in database.")
        
        return book_data
        

    def get_all_books_list(self, book_id):
        """ This method returns list of all books in database. It can be used to display all books in GUI and makes possible to manage on the books (searching, deleting, updating etc.)

        Args:
            book_id (int): Unique identifier of the book.

        Raises:
            exc.BookNotFoundError: _description_
            exc.BookError: _description_

        Returns:
            list: List of all books in database.
        """
        current_data = self.json_service.load_json_file()
        all_books = []
        book_found = False

        for book in current_data:
            if book["book_id"] == book_id:
                try:
                    all_books.append(book)
                    book_found = True
                except KeyError:
                    raise exc.BookNotFoundError(f"Book with ID {book_id} not found in database.")
            if not book_found:
                raise exc.BookNotFoundError(f"Book with ID {book_id} not found in database.")
        return all_books


    def update_book_data(self, book_id, field, new_value):
        """ Update an existing book record in the JSON file with new data.
        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_book_data(book_id)
        book_found = False

        if not new_value:
            raise exc.FileError("This exception requires sth better. And this validation needs to be in similar methods. New value to update book record is incorrect or not exists.")

        for book in current_data:
            if book["book_id"] == book_id:
                try:
                    book[field] = new_value
                    book_found = True
                except KeyError:
                    raise exc.BookValidationError("Book ID is invalid or it's an emppty value.")

        if not book_found:
            raise exc.BookNotFoundError("New value to update book record is incorrect or empty value.")
        
        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"Data in book with book ID: {book_id} has been changed in field: {field}."


    
    def delete_book_by_id(self, book_id):
        """ This method is for deleting book by id from the JSON file. It checks permission to delete data.
        """
        self.authorisation.check_permission("delete_book")
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_book_data(book_id)

        book_deleted = False
        for book in current_data:
            if book["book_id"] == book_id:
                current_data.remove(book)
                book_deleted = True
                break

        if not book_deleted:
            raise exc.BookError(f"Book with ID: {book_id} couldn't be removed from database.")
        
        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"Book with ID: {book_id} has beed deleted from the library. "