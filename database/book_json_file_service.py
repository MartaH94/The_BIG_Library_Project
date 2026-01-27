"""
________________________________________________________
database.book_json_file_service
========================================================
Service class for managing book data in a JSON file.
________________________________________________________

Book JSON storage service.

This module provides a service layer for managing book records stored in a JSON file.
It supports adding, retrieving, updating, and deleting book entries while relying on
a lower‑level JSON file service for schema validation, loading, and saving. It is used
to maintain the library’s book collection in a consistent and safe way

"""

import exceptions as exc
from database.json_files_major_services import JsonFilesService
from utils.config import THE_LIBRARY_FILE_PATH


class BookJsonFileService:
    """High-level operations for books stored in a JSON file.

    Works with JsonFilesService to load, validate, and modify book data while exposing
    convenient methods for interacting with the library’s book collection.
    """

    def __init__(
        self,
        json_service: JsonFilesService,
        file_path=THE_LIBRARY_FILE_PATH,
    ):
        self.json_service = json_service
        self.file_path = file_path

    def get_book_data(self, book_id):
        """Retrieve a single book record by its ID.

        Args:
            book_id (str): Unique book identifier.

        Returns:
            dict: The matching book record.

        Raises:
            exc.BookNotFoundError: If no book with the given ID is found.
        """
        current_data = self.json_service.load_json_file()
        book_found = False
        book_data = None

        for book in current_data:
            if book["book_id"] == book_id:
                book_data = book
                book_found = True

        if not book_found:
            raise exc.BookNotFoundError(
                f"Book with {book_id} does not exists in database."
            )

        return book_data

    def add_book_data(self, book_data):
        """Add a new book record to the database.

        Validates the incoming data against the schema and ensures the book ID is unique.

        Args:
            book_data (dict): New book record.

        Returns:
            str: Confirmation message.

        Raises:
            exc.DataError: If the payload is missing.
            exc.DataTypeError: If the record is not a dict.
            exc.BookError: If the ID already exists.
            exc.BookValidationError: If schema validation fails.
        """
        current_data = self.json_service.load_json_file()
        validated_book_data = self.json_service.validate_against_schema(book_data)
        book_id = book_data["book_id"]

        if not book_data:
            raise exc.DataError("Book data to save is missing or it's incorrect.")

        if not isinstance(book_data, dict):
            raise exc.DataTypeError(
                "Book data type is incorrect. Book data must be a dict type."
            )

        for book in current_data:
            if book["book_id"] == book_id:
                raise exc.BookError(
                    f"Book with ID: {book["book_id"]} exists in the database. ID number must be unique value."
                )

        if not validated_book_data:
            raise exc.BookValidationError(
                "Validation failed. Book data doesn't match database file schema."
            )
        else:
            current_data.append(book_data)

        self.json_service.write_json_data(current_data)

        return "New book record added to the database without errors."

    def get_all_books_list(self, book_id):
        """Return all books that match a given ID.

        Note : Typical “get all books” functions do not filter by ID.

        Args:
            book_id (int): Book identifier to filter.

        Returns:
            list: List of matching books.

        Raises:
            exc.BookNotFoundError: If no matching books are found.

        """
        current_data = self.json_service.load_json_file()
        self.get_book_data(book_id)
        all_books = []
        book_found = False

        for book in current_data:
            if book["book_id"] == book_id:
                try:
                    all_books.append(book)
                    book_found = True
                except KeyError:
                    raise exc.BookNotFoundError(
                        f"Book with ID {book_id} not found in database."
                    )
            if not book_found:
                raise exc.BookNotFoundError(
                    f"Book with ID {book_id} not found in database."
                )
        return all_books

    def update_book_data(self, book_id, field, new_value):
        """Update a specific field in an existing book record.

        Loads the data, checks the book exists, updates the field, validates the file
        contents, and persists the modified data.

        Args:
            book_id (int): Identifier of the book to modify.
            field (str): Field name to update.
            new_value (str): New value to write.

        Returns:
            str: Confirmation message.

        Raises:
            exc.BookValidationError: If the new value is empty or invalid.
            exc.BookNotFoundError: If the book or field is missing.
        """
        current_data = self.json_service.load_json_file()
        self.get_book_data(book_id)
        book_found = False

        if not new_value:
            raise exc.BookValidationError(
                "New value to update book record is incorrect or is empty value."
            )

        for book in current_data:
            if book["book_id"] == book_id:
                try:
                    book[field] = new_value
                    book_found = True
                except KeyError:
                    raise exc.BookValidationError(
                        "Book ID is invalid or it's an emppty value."
                    )

        if not book_found:
            raise exc.BookNotFoundError(
                "New value to update book record is incorrect or empty value."
            )

        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return (
            f"Data in book with book ID: {book_id} has been changed in field: {field}."
        )

    def delete_book_by_id(self, book_id):
        """Delete a book record by its ID.

        Loads current data, removes the matching entry, validates the updated dataset,
        and writes the result back to the file.

        Args:
            book_id (int): Book identifier.

        Returns:
            str: Confirmation message.

        Raises:
            exc.BookError: If the book cannot be removed.
        """
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
            raise exc.BookError(
                f"Book with ID: {book_id} couldn't be removed from database."
            )

        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"Book with ID: {book_id} has beed deleted from the library. "
