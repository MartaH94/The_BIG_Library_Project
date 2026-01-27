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
        file_path=PROGRAM_USERS_FILE_PATH,
    ):
        self.json_service = json_service
        self.file_path = file_path

    def get_user_data(self, user_id):
        """Retrieve a user data record from the JSON file by user ID. It can be used to display user details in GUI.
        Args:
            user_id (int): The ID of the user to retrieve.
        Returns:
            user_data (dict) - The data for the specified user returned as a dictionary.
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
        """Add a new user record to the JSON file. This method checks user's permissions to edit data, loads current data from file, validates new user data against schema,
            checks for unique user ID, appends new user data to current data, and writes updated data back to the file. It can be used to create a new user record.
        Args:
            user_data (dict): The user data to add.
        Returns:
            str - Confirmation message with the new user's ID.
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
        """Retrieve all user records from the JSON file that match the given login name. It can be used to display user details in GUI.
        Args:
            user_login_name (str): The login name of the user to retrieve. For example john_example3
        Returns:
            list - A list of user records matching the login name.
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
        """Update an existing user record in the JSON file with new data. This method is about to work on previously verified file using load_json_file method() from
            json_files_major_services module, which returns checked and ready to work json file. Also this method validates data and save changes in the file.
        Args:
            user_id (int): The ID of the user to update.
            field (str): The field to update.
            new_value (str): The new value to update the field with.
        Returns:
            str - Confirmation message indicating successful update.
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
        """This method is for deleting user by id from the JSON file. It checks permission to delete data.

        Args:
            user_id (int): The ID of the user to delete.
        Returns:
            str - Confirmation message indicating successful deletion.
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
