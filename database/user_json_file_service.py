import json
import exceptions as exc

from utils.config import PROGRAM_USERS_FILE_PATH
from database.json_files_major_services import JsonFilesService
from services.authorisation_service import UserAuthorisation

class UsersJsonFileService():
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=PROGRAM_USERS_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def get_user(self, user_id):
        pass

    def add_user(self, user_data):
        pass

    def all_users_list(self):
        pass


    def update_user_record_id(self, user_id, field, new_value):
        """ Update an existing user record in the JSON file with new data. This method is about to work on previouly checked file using load_json_file method() from 
            json_files_major_services module, which returns checked and ready to work json file. Also this method validates data and save changes in the file. 
        Args:
            user_id (str): The ID of the user to update.
            field (str): The field to update.
            new_value (str): The new value to update the field with.
        """
        current_data = self.json_service.load_json_file()
        user_found = False

        for user in current_data:
            if user["id"] == user_id:
                try:
                    user[field] = new_value
                    user_found = True
                except KeyError:
                    raise exc.UserValidationError("User id is invalid or it's empty value")
            if not user_found:
                raise exc.UserNotFoundError(f"User with id: {user_id} not found in users database.")
            
        self.json_service.validate_file_data()
        self.json_service.write_json_data(current_data)
                

    def update_file_data(self, user_id, field, new_value):
        """This method is for update users data in the JSON file. It checks user's permissions to edit data, checks if file exits and returns confirmation to the GUI.
        """

        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checking()
        self.update_user_record_id(user_id, field, new_value)
        
        return "In Gui confirmation changes made succesfully and saved in file"
    




    def delete_data_from_file(self, user_id): # this method requires review. also add method: delete_user_by_id
        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()

        if not user_id:
            raise exc.UserValidationError("User's id is invalid or it's empty value.")
        
        user_id_found = False
        for user in current_data:
            if user["id"] == user_id:
                current_data.remove(user)
                user_id_found = True

            if not user_id_found:
                raise exc.UserNotFoundError(f"User with id {user_id} does not exist in user data json file.")


