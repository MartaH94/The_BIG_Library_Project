"""
________________________________________________________
database.book_json_file_service
========================================================
Service class for managing book data in a JSON file.
________________________________________________________

Book JSON storage service.

This module provides a service layer for managing book records stored in a JSON file.
It supports adding, retrieving, updating, and deleting book entries while relying on
a lower-level JSON file service for schema validation, loading, and saving. It is used
to maintain the library's book collection in a consistent and safe way

"""

import database.database_schemes as schema
import exceptions as exc
from database.json_files_major_services import JsonFilesService
from utils.config import THE_LIBRARY_FILE_PATH


class BookJsonFileService:
    """High-level operations for books stored in a JSON file.

    Works with JsonFilesService to load, validate, and modify book data while exposing
    convenient methods for interacting with the library's book collection.
    """

    def __init__(
        self,
        json_service: JsonFilesService,
        file_path=THE_LIBRARY_FILE_PATH,
    ):
        self.json_service = json_service
        self.file_path = file_path

    def get_book_data(self, book_id):
        """Return a single book record by its ID.
        Args:
            book_id (int): ID of the book to retrieve.
        Returns:
            book_data (dict): The matching book record.
        """

        current_data = self.json_service.load_json_file()
        book_found = False
        book_data = None

        if book_id is None:
            raise exc.ValidationError(
                "Book ID is missing or it's an empty value. Getting book data not possible."
            )

        for book in current_data:
            if book["book_id"] == book_id:
                book_data = book
                book_found = True
                break

        if not book_found:
            raise exc.BookNotFoundError(
                f"Book with {book_id} does not exists in database."
            )

        return book_data

    def add_book_data(self, book_data):
        """Add a new book record to the JSON file.
        Args:
            book_data (dict): The book data to add.
        Returns:
            str: Message with confirmation of success.
        """

        current_data = self.json_service.load_json_file()

        if not book_data:
            raise exc.ValidationError("Book data to save is missing.")

        if not isinstance(book_data, dict):
            raise exc.DataTypeError(
                "Book data type is incorrect. Book data must be a dict type."
            )

        try:
            validated_book_data = self.json_service.validate_against_schema(
                book_data, schema.book_schema
            )
        except exc.ValidationError as e:
            raise exc.BookValidationError(
                f"Validation failed. Book data doesn't match database file schema: {e}"
            )

        if not isinstance(validated_book_data, dict):
            raise exc.BookValidationError("Validated book data is not a dictionary.")

        book_id = validated_book_data["book_id"]

        for book in current_data:
            if book.get("book_id") == book_id:
                raise exc.BookError(
                    f"Book with ID: {book_id} exists in the database. Book ID number must be unique value."
                )

        current_data.append(validated_book_data)
        self.json_service.write_json_data(current_data)
        return f"Added new book to data base with ID: {book_id}."

    def get_all_books_list(self):
        """Return a list of all book records in the JSON file.
        Returns:
            all_books (list): A list of all book records.
        """

        current_data = self.json_service.load_json_file()
        all_books = []

        for book in current_data:
            if isinstance(book, dict) and "book_id" in book:
                all_books.append(book)

        if not all_books:
            raise exc.BookNotFoundError("No book found in the database.")

        return all_books

    def update_book_data(self, book_id, field, new_value):
        """Update a specific field of a book record by its ID.
        Args:
            book_id (int): ID of the book to update.
            field (str): The field name to update.
            new_value: The new value to set for the specified field.
        Returns:
            str: Message with confirmation of success.
        """

        current_data = self.json_service.load_json_file()
        book_id_found = False

        if book_id is None:
            raise exc.ValidationError("Book ID is missing or it's an empty value.")

        if field is None:
            raise exc.ValidationError(
                "The field value is missing or it's an empty value."
            )

        if new_value is None:
            raise exc.ValidationError(
                "New value to update book record is incorrect or is empty value."
            )

        for book in current_data:
            if book.get("book_id") == book_id:
                if field not in book:
                    raise exc.ValidationError(
                        f"The field '{field}' is missing in this book entry."
                    )

                book[field] = new_value

                try:
                    self.json_service.validate_against_schema(book, schema.book_schema)
                except exc.ValidationError as e:
                    raise exc.BookValidationError(
                        f"Validation failed while updating book data: {e}"
                    )

                book_id_found = True
                break

        if not book_id_found:
            raise exc.BookNotFoundError(
                f"Book with ID: {book_id} not found in database."
            )

        self.json_service.write_json_data(current_data)
        return f"New data value has been saved for book with ID: {book_id}"

    def delete_book_by_id(self, book_id):
        """Delete a book record from the database by its ID.
        Args:
            book_id (int): ID of the book to delete.
        Returns:
            str: Message with confirmation of success.
        """

        current_data = self.json_service.load_json_file()
        book_deleted = False

        if book_id is None:
            raise exc.ValidationError("Book ID is missing or it's an empty value.")

        for book in current_data:
            if book.get("book_id") == book_id:
                current_data.remove(book)
                book_deleted = True
                break

        if not book_deleted:
            raise exc.BookNotFoundError(
                f"Book with ID: {book_id} could not be removed from the database."
            )

        self.json_service.write_json_data(current_data)
        return f"Book with ID: {book_id} has been deleted from the database."
