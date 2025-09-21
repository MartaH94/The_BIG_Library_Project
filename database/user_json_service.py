import json
import exceptions as exc

from utils.config import PROGRAM_USERS_FILE_PATH
from database.JSON_files_service import JsonFilesService
from services.authorisation_service import UserAuthorisation

class UsersJsonFileService():
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=PROGRAM_USERS_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def update_file_data(self, user_id, field, new_value):
        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checkout()
        current_data = self.json_service.read_json_file()

        if not new_value:
            return "New value field, can not be an empty field."
        
        user_id_found = False

        for user in current_data:
            if user["id"] == user_id:
                try:
                    user[field] = new_value
                    user_id_found = True
                except KeyError:
                    raise exc.InvalidFieldError(f"Field {field} does not exist in the user data file")
                
            if not user_id_found:
                raise exc.UserNotFoundError("User doesn not exists in users json file.")
            
        self.json_service.write_json_data(current_data)
        return "In Gui confirmation changes made succesfully and saved in file"
    
    def delete_data_from_file(self, user_id):
        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checkout()
        current_data = self.json_service.read_json_file()

        if not user_id:
            raise exc.UserValidationError("User's id is invalid or it's empty value.")
        
        user_id_found = False
        for user in current_data:
            if user["id"] == user_id:
                current_data.remove(user)
                user_id_found = True

            if not user_id_found:
                raise exc.UserNotFoundError(f"User with id {user_id} does not exist in user data json file.")


