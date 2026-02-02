"""
________________________________________________________
database.user_json_file_service
========================================================
Service class for managing user records in a JSON file.
________________________________________________________

User JSON storage service.

This module provides a thin service layer for managing user records stored in a JSON
file. It offers simple helpers to load, add, query, update, and delete users while
leveraging a lower-level JSON file service for I/O, validation, and persistence.

"""

import exceptions as exc
from database.json_files_major_services import JsonFilesService
from utils.config import PROGRAM_USERS_FILE_PATH


class UsersJsonFileService:
    """High-level operations for user records stored in a JSON file.

    This service coordinates with `JsonFilesService` for file access and schema checks,
    exposing simple methods to read and modify user data.
    """

    def __init__(
        self,
        json_service: JsonFilesService,
        file_path: str = PROGRAM_USERS_FILE_PATH,
    ):
        self.json_service = json_service
        self.file_path = file_path

    def get_user_data(self, user_id):
        """Return a single user record by ID.

        Args:
            user_id (int): ID of the user to retrieve.

        Returns:
            dict: The matching user record.

        Raises:
            exc.UserNotFoundError: If the user is not present in the database.
        """
        current_data = self.json_service.load_json_file()
        user_found = False
        user_data = None

        for user in current_data:
            if user["id"] == user_id:
                user_data = user
                user_found = True

        if not user_found:
            raise exc.UserNotFoundError(
                f"User with {user_id} does not exist in database"
            )

        return user_data

    def add_user_data(self, user_data):
        """Add a new user record.

        Validates the incoming record against the schema, enforces unique ID,
        appends it to the list, and persists changes.

        Args:
            user_data (dict): User data to insert.

        Returns:
            str: Confirmation message with the new user's ID.

        Raises:
            exc.DataError: If the input payload is missing.
            exc.DataTypeError: If the payload is not a dict.
            exc.UserError: If the user ID already exists.
            exc.UserValidationError: If validation against the schema fails.
        """
        current_data = self.json_service.load_json_file()
        validated_data = self.json_service.validate_against_schema(user_data)
        user_id = user_data["id"]

        if not user_data:
            raise exc.DataError("User data to add is missing.")

        if not isinstance(user_data, dict):
            raise exc.DataTypeError(
                "User data type is incorrect. User data must be a dict type."
            )

        for user in current_data:
            if user["id"] == user_id:
                raise exc.UserError(
                    f"User with ID: {user_id} already exists in the database. User ID must be unique value."
                )

        if not validated_data:
            raise exc.UserValidationError(
                f"Validation new user data {user_data} does not match file schema."
            )
        else:
            current_data.append(user_data)

        self.json_service.write_json_data(current_data)

        return f"Added new user to database with ID: {user_id}"

    def get_all_users_list(self, user_login_name):
        """Return all user records matching the given login name.

        Args:
            user_login_name (str): Login name to filter by (e.g., 'john_example3').

        Returns:
            list: All matching user records.

        Raises:
            exc.UserNotFoundError: If no users match the provided login name.
        """
        current_data = self.json_service.load_json_file()
        self.get_user_data(user_login_name)
        all_users = []
        user_found = False

        for user in current_data:
            if user["user_name"] == user_login_name:
                try:
                    all_users.append(user)
                    user_found = True
                except KeyError:
                    raise exc.UserNotFoundError(
                        f"User with login: {user_login_name} not found in database."
                    )
            if not user_found:
                raise exc.UserNotFoundError(
                    f"User with login: {user_login_name} not found in database."
                )

        return all_users

    def update_user_data(self, user_id, field, new_value):
        """Update a field on the specified user.

        Loads the current data, ensures the user exists, updates the field,
        validates the file contents, and persists changes.

        Args:
            user_id (int): ID of the user to update.
            field (str): Field name to modify.
            new_value (str): New value to set.

        Returns:
            str: Confirmation message.

        Raises:
            exc.DataError: If the new value is missing.
            exc.UserNotFoundError: If the user or field is not found.

        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_user_data(user_id)
        user_found = False

        if not new_value:
            raise exc.DataError("New value to update user data is missing.")

        for user in current_data:
            if user["id"] == user_id:
                try:
                    user[field] = new_value
                    user_found = True
                except KeyError:
                    raise exc.UserNotFoundError(
                        f"User with ID: {user_id} not found in database."
                    )
            if not user_found:
                raise exc.UserNotFoundError(
                    f"User with ID: {user_id} not found in database."
                )

        self.json_service.validate_file_data()
        self.json_service.write_json_data(current_data)
        return f"For user with ID: {user_id}, data updated successfully."

    def delete_user_by_id(self, user_id):
        """Delete a user by ID.

        Loads the current data, removes the matching record,
        validates the file state, and persists changes.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            str: Confirmation message.

        Raises:
            exc.UserError: If the user could not be removed.
        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_user_data(user_id)
        user_deleted = False

        for user in current_data:
            if user["id"] == user_id:
                current_data.remove(user)
                user_deleted = True
                break

        if not user_deleted:
            raise exc.UserError(
                f"User with ID: {user_id} couldn't be removed from database."
            )

        self.json_service.validate_file_data()
        self.json_service.write_json_data(current_data)

        return f"User with ID {user_id} deleted from database."
