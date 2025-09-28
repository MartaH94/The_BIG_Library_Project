"""
Database service to handle JSON file operations such as reading, writing, appending data, checking file existence, 
creating backups, and validating file structure and fields.
    _
"""

import json
import utils.config as config
import exceptions as exc
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
        Returns: list - Data from the JSON file."""
        self.file_exists_checkout()
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError:
            return []
        
    def write_json_data(self, data):
        self.file_exists_checkout()

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)


    def append_data_to_file(self, data_to_append): # in progress
        """ Append new data to the JSON file.
        Args: data_to_append (dict) - Data to append to the JSON file.
        Returns: str - confirmation message."""
        self.file_exists_checkout()
        current_data = self.read_json_file() 
        current_data.append(data_to_append)

        self.validate_file_data()
        self.write_json_data(current_data)

        return f"Data had been saved to file: {self.file_path.name}"

    

    def validate_file_data(self, field_name):
        if not self.file_path.exists():
            raise exc.FileNotFound("File does not exist in program data directory.")
        
        self.file_exists_checkout()
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read the file: {e} from program data directory.")
        

        field_found = False

        for item in data:
            if isinstance(item, dict) and field_name in item:
                field_found = True
                break

            if not isinstance(item, list):
                raise exc.FileError("File should be a list of items. Check file structure.")
        
            if not field_found:
                raise exc.InvalidFieldError(f"The field {field_name} not found in the file: {self.file_path.name}")
        
        return f"File validation successful. Validated file {self.file_path.name}"

    def create_backup_file(self):
        if not self.file_path.exists():
            raise exc.FileNotFound("File not found in the folder.")
        
        name = self.file_path.stem
        subfolder_backup = config.BACKUP_FILES_DIRECTORY/ name

        if not subfolder_backup.exists():
            subfolder_backup.mkdir(parents=True, exist_ok=True)

        alias = config.PROJECT_ALIAS
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"
        backup_file_path = subfolder_backup/backup_file_name

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read JSON file: {e}")
            
        with backup_file_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4)

        return backup_file_path



    


        

# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database