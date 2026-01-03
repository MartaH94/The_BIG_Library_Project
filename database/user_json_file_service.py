"""
Docstring for database.user_json_file_service
Service class for managing user records in a JSON file.

TO DO HERE:
- Implement method to retrieve all users. <-- Done.
- Implement method to delete user by ID. <-- Done.
- Reimplement delete_data_from_file method. <-- In progress.
- Review permission checks in all methods.
- Review imports.
- Review docstrings.


"""

import json
import exceptions as exc

from utils.config import PROGRAM_USERS_FILE_PATH
from database.json_files_major_services import JsonFilesService
from services.authorisation_service import UserAuthorisation
from services.authorisation_service import user_permissions

class UsersJsonFileService():
    """ Service class for managing user records in a JSON file. This class provides methods to add, retrieve, update, and delete user records,
        while ensuring data validation and user authorisation.
    """
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=PROGRAM_USERS_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path


    def get_user_data(self, user_id):
        """ Retrieve a user data record from the JSON file by user ID. 
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
            raise exc.UserNotFoundError(f"User with {user_id} does  not exist in database")        

        return user_data
    

    def add_user(self, user_data):  
        """ Add a new user record to the JSON file. This method checks user's permissions to edit data, loads current data from file, validates new user data against schema,
            checks for unique user ID, appends new user data to current data, and writes updated data back to the file.
        Args:
            user_data (dict): The user data to add.
        Returns:
            str - Confirmation message with the new user's ID.
        """
        self.authorisation.check_permission("edit_data")
        current_data = self.json_service.load_json_file()
        validated_data = self.json_service.validate_against_schema(user_data)
        user_id = user_data["id"]

        if not user_data:
            raise exc.DataError("User data its empty value or its misisng. Provide correct data.")
        
        if not isinstance(user_data, dict):
            raise exc.DataTypeError("User data must be a dictionary.")

        for user in current_data:
            if user["id"] == user_id:
                raise exc.UserError(f"User with {user_id} already exists in database. Each user needs unique ID.")

        if not validated_data:
            raise exc.ValidationError(f"Validation new user data {user_data} does not match file schema.")
        else:
            current_data.append(user_data)
        
        self.json_service.write_json_data(current_data)

        return f"Added new user to database with ID: {user_id}"


    def all_users_list(self, user_login_name):
        """ Retrieve all user records from the JSON file that match the given login name. 
        Args:
            user_login_name (str): The login name of the user to retrieve.
        Returns:
            list - A list of user records matching the login name.
        """
        self.authorisation.check_permission("view_data")
        current_data = self.json_service.load_json_file()
        all_users = []

        user_found = False
        for user in current_data:
            if user["user_name"] == user_login_name:
                try:
                    all_users.append(user)
                    user_found = True
                except KeyError:
                    raise exc.UserNotFoundError(f"No user with name: {user["user_name"]} in library database.")
            if not user_found:
                raise exc.UserError(f"No user in database. Impossible to view data of user: {user["user_name"]} ")
            
        return all_users


    def update_user_record_id(self, user_id, field, new_value):
        """ Update an existing user record in the JSON file with new data. This method is about to work on previously verifiedfile using load_json_file method() from 
            json_files_major_services module, which returns checked and ready to work json file. Also this method validates data and save changes in the file. 
        Args:
            user_id (int): The ID of the user to update.
            field (str): The field to update.
            new_value (str): The new value to update the field with.
        Returns:
            str - Confirmation message indicating successful update.
        """
        current_data = self.json_service.load_json_file()
        user_found = False

        for user in current_data:
            if user["id"] == user_id:
                try:
                    user[field] = new_value
                    user_found = True
                except KeyError:
                    raise exc.UserValidationError("User's ID is invalid or it's empty value")
            if not user_found:
                raise exc.UserNotFoundError(f"User with id: {user_id} not found in users database.")
            
        self.json_service.validate_file_data()
        self.json_service.write_json_data(current_data)
        return f"For user with ID: {user_id}, data updated successfully."
                

    def update_file_data(self, user_id, field, new_value):
        """This method is for update users data in the JSON file. It checks user's permissions to edit data, checks if file exits and returns confirmation message.
        Args:
            user_id (int): The ID of the user to update.
            field (str): The field to update.
            new_value (str): The new value to update the field with.
        Returns:
            str - Confirmation message indicating successful update.
        """
        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checking()
        self.update_user_record_id(user_id, field, new_value)
        return "Changes in the file made succesfully and saved"
    

    def delete_user_by_id(self, user_id):
        """This method is for deleting user by id from the JSON file. It checks permission to delete data.
            
        Raises:
            exc.UserNotFoundError: _description_
        """
        self.authorisation.check_permission("delete_data")
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
            raise exc.UserError(f"User {user_id} couldn't be removed from database.")

        self.json_service.validate_file_data()
        self.json_service.write_json_data(current_data)
                
        return f"User with ID {user_id} deleted from database."
                

    def delete_data_from_file(self, user_id, field_to_delete): 
        """This method is for deleting user data from database. 

        Args:
            user_id (_type_): _description_
            field_to_update (): 

        Raises:
            exc.UserValidationError: _description_
            exc.UserNotFoundError: _description_
        """


        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        user_data = self.get_user_data()
        field_found = False


        for user in current_data:
            if user["id"] == user_id:
                try:
                    current_data.remove(user_data)
                    field_found = True
                except KeyError:
                    raise exc.DataError("User data coudn't be deleted from database.")


        


