"""
Database service to handle JSON file operations such as reading, writing, appending data, checking file existence, 
creating backups, and validating file structure and fields.
    _
"""

import json
import utils.config as config
import exceptions as exc
from database import database_schemes
from pathlib import Path
from datetime import datetime


class JsonFilesService():
    """ Service to handle JSON file operations."""

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def file_exists_checking(self):
        """ Check if the JSON file exists; if not, create new file with empty list.
        Returns: str - Message indicating the status of the file."""
        file_content = []

        if not self.file_path.exists():
            self.write_json_data(file_content)
            return "File didn't exist. Created new file with empty list."
        elif self.file_path.stat().st_size == 0:
                self.write_json_data(file_content)
                return "File was empty. Created new file with empty list."
        else:
            return "The file exists. You can continue."


    def read_json_file(self):
        """ Read and return data from the JSON file.
        Returns: list - Data read from the JSON file. If the file is empty, returns an empty list."""
        self.file_exists_checking()
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                if self.file_path.stat().st_size == 0:
                    return []
                data = json.load(f)
                if data is None:
                    return []
                if not isinstance(data, list):
                    raise exc.FileError("File should be a list of items. Check file structure.")
                return data
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read the file: {e} from program data directory.")
        
        
    def write_json_data(self, data):
        """ Write data to the JSON file.
        Args: data (list) - Data to write to the JSON file. """
        self.file_exists_checking()
        if data is None:
            raise exc.FileError("File data is None. Cannot save data to the file.")
        if not isinstance(data, list):
            raise exc.FileError("Data is not a list. Cannot save data to the file.")        
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)


    def append_data_to_file(self, data_to_append):
        """ Append new data to the JSON file.
        Args: data_to_append (dict) - Data to append to the JSON file must be dictionary of data to append like new user data or new book data, etc.
        Returns: str - confirmation message."""
        current_data = self.read_json_file() 
        if not data_to_append:
            raise exc.ValidationError("Data is empty. Cannot save dictionary to the file.")
        if not isinstance(data_to_append, dict):
            raise exc.FileError("Data is not a dictionary. Cannot save data to the file.")
        
        current_data.append(data_to_append)
        self.write_json_data(current_data)
        return f"Data had been added and saved to file: {self.file_path.name}"
      

    def validate_file_data(self, field_name):
        """ Validate that the JSON file contains the specified field in its items.
        Args: field_name (str) - The field name to validate in the JSON file items
        Returns: str - Confirmation message if validation is successful."""
        if not self.file_path.exists():
            raise exc.FileNotFound("File not found. Cannot find file in the directory.")
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            if self.file_path.stat().st_size == 0:                    
                raise exc.ValidationError("File is empty. Check your file data.")                
            if not isinstance(data, list):
                raise exc.FileError("File should be a list of items. Check file structure.")        
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read the file: {e} from program data directory.")
                
        field_found = False
        for item in data:
            if not isinstance(item, dict):
                raise exc.FileError("File should be a list of items. Check file structure.")  
            
            for field, expected_type in database_schemes.items():
                if field not in item:
                    raise exc.InvalidFieldError(f"The field {field} not found in the file: {self.file_path.name}")
                if not isinstance(item[field], expected_type):
                    raise exc.ValidationError(f"Incorrect data type for field: {field}.")
            if  field_name in item:
                field_found = True             
        if not field_found:
                raise exc.InvalidFieldError(f"The field {field_name} not found in the file: {self.file_path.name}")
        return f"File validation successful. Validated file {self.file_path.name}"
        # I'm not checking if the file is empty in that function. Add an if statement in code of this function.


    def create_backup_file(self):
        """ Create a backup of the current JSON file with a timestamped filename in the backup directory.
        Returns: Path - The path to the created backup file.
        """
        if not self.file_path.exists():
            raise exc.FileNotFound("File does not exist in the directory.")
        name = self.file_path.stem
        subfolder_backup = config.BACKUP_FILES_DIRECTORY/ name

        if not subfolder_backup.exists():
            subfolder_backup.mkdir(parents=True, exist_ok=True)

        alias = config.PROJECT_ALIAS
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"
        backup_file_path = subfolder_backup/backup_file_name
        data = self.read_json_file()
            
        with backup_file_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4, sort_keys=True)
        return backup_file_path



    


        

# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database