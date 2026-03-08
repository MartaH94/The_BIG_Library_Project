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

import database.database_schemes as schema
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
        file_path=PROGRAM_USERS_FILE_PATH,
    ):
        self.json_service = json_service
        self.file_path = file_path

    def get_user_data(self, user_id):
        """Return a single user record by its ID.
        Args:
            user_id (int): ID of the user to retrieve.
        Returns:
            user_data (dict): The matching user record.
        """
        current_data = self.json_service.load_json_file()
        user_found = False
        user_data = None

        if user_id is None:
            raise exc.ValidationError(
                "User ID is missing or it's an empty value. Getting user data not possible.")

        for user in current_data:
            if user["id"] == user_id:
                user_data = user
                user_found = True
                break

        if not user_found:
            raise exc.UserNotFoundError(
                f"User with {user_id} does not exist in database."
            )

        return user_data

    def add_user_data(self, user_data):
        """Add a new user record to the JSON file.
        Args:
            user_data (dict): The user data to add.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()

        if not user_data:
            raise exc.ValidationError("User data to add is missing.")

        if not isinstance(user_data, dict):
            raise exc.DataTypeError(
                "User data type is incorrect. User data must be a dict type."
            )

        user_id = user_data["id"]

        for user in current_data:
            if user["id"] == user_id:
                raise exc.UserError(
                    f"User with ID: {user_id} already exists in the database. User ID must be unique value."
                )
        validated_user_data = self.json_service.validate_against_schema(
            user_data, schema.user_schema)

        if not validated_user_data:
            raise exc.UserValidationError(
                "Validation failed. User data doesn't match the schema."
            )
        else:
            current_data.append(validated_user_data)

        self.json_service.write_json_data(current_data)

        return f"Added new user to database with ID: {user_id}."

    def get_all_users_list(self):
        """Retrieve all user records from the database.
        Returns:
            all_users (list): List of all user records.
        """
        current_data = self.json_service.load_json_file()
        all_users = []
        user_found = False

        for user in current_data:
            if user["user_name"]:
                all_users.append(user)
                user_found = True
            else:
                raise exc.UserNotFoundError(
                    "User not found in database.")
            if not user_found:
                raise exc.UserNotFoundError(
                    "User not found in database.")

        return all_users

    def update_user_data(self, user_id, field, new_value):
        """Update a single user record by its ID.
        Args:
            user_id (int): ID of the user to update.
            field (str): The field to update.
            new_value: The new value to set.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()
        user_found = False

        if user_id is None:
            raise exc.ValidationError(
                "User ID is missing or it's an empty value.")

        if field is None:
            raise exc.ValidationError(
                "Field value is missing or it's an empty value.")

        if new_value is None:
            raise exc.ValidationError(
                "New value to update data is missing or it's an empty value.")

        for user in current_data:
            if user.get("user_id") == user_id:
                if field not in user:
                    raise exc.ValidationError(
                        f"The field '{field}' is missing in this user entry.")

            user[field] = new_value
            user_found = True
            break

        if not user_found:
            raise exc.UserNotFoundError(
                f"User with ID: {user_id} not found in database.")

        self.json_service.write_json_data(current_data)
        return f"For user with ID: {user_id}, data updated successfully."

    def delete_user_by_id(self, user_id):
        """ Delete a user record by its ID.
        Args:
            user_id (int): ID of the user to delete.
        Returns:
            str: Message with confirmation of success.
        """
        current_data = self.json_service.load_json_file()
        user_deleted = False

        if user_id is None:
            raise exc.ValidationError(
                "User ID is missing ir it's an empty value.")

        for user in current_data:
            if user["id"] == user_id:
                current_data.remove(user)
                user_deleted = True
                break

        if not user_deleted:
            raise exc.UserError(
                f"User with ID: {user_id} not found in database and couldn't be removed from database."
            )

        self.json_service.write_json_data(current_data)
        return f"User with ID {user_id} deleted from database."
