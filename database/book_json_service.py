import json
import utils.config as config
import exceptions as exc

from utils.config import THE_LIBRARY_FILE_PATH
from database.JSON_files_service import JsonFilesService
from services.authorisation_service import UserAuthorisation

class BookJsonFileService():
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=THE_LIBRARY_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def update_file_data(self, book_id, field, new_value):
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