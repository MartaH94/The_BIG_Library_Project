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

    def __init__(self, file_path: Path, schema: dict):
        self.file_path = file_path
        self.schema = schema

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
            return "File verified: existing or newly created with empty list."



    def load_json_file(self):   # previously read_json_file; method to read json file content and return data for further process
        """Read JSON file content.
        Returns: list - Data read from the JSON file."""
        self.file_exists_checking()
        
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise exc.FileError("File should be a list of items. Check file structure.")
                return data
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read the file: {e} from program data directory.")
        
        
    def write_json_data(self, data):
        """ Write data to the JSON file.
        Args: data (list) - Data to write to the JSON file. """

        if not data:
            raise exc.FileError("Data is empty. Cannot save empty data to the file.")
        if not isinstance(data, list):
            raise exc.FileError("Data is not a list. Cannot save data to the file.") 
        self.validate_against_schema(data,[self.schema])       
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)


    def append_data_to_file(self, data_to_append):
        """ Append new data to the JSON file.
        Args: data_to_append (dict) - Data to append to the JSON file must be dictionary of data to append like new user data or new book data, etc.
        Returns: str - confirmation message."""

        current_data = self.load_json_file() 
        if not data_to_append:
            raise exc.ValidationError("New record is empty. Cannot save dictionary to the file.")
        
        self.validate_against_schema(data_to_append, self.schema)
        current_data.append(data_to_append)
        self.write_json_data(current_data)
        return f"Data had been added and saved to file: {self.file_path.name}"
      


    def validate_against_schema(self, data, schema):
        """The method to validate values type and structure against the given schema. """
        
        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise exc.ValidationError(f"Given value {data} should be a dictionary")
            for key, subschema in schema.items():
                if key not in data:
                    raise exc.ValidationError(f"Missing key {key} in {subschema}")
                self.validate_against_schema(data[key], subschema)
        else:
            if not isinstance(data, schema):
                raise exc.ValidationError("Wrong type ")


    def validate_file_data(self): #collects data from file loading function, check if data in file is correct, return true/false or exception when data is incorrect.
        """ Veryfying if the list of items in the JSON file is not empty and each item matches the expected schema."""
        self.file_exists_checking()
        file_content = self.load_json_file()

        if not file_content:
            raise exc.ValidationError(f"File {self.file_path.name} is empty. Cannot validate fields in an empty file.")  
        for index, item in enumerate(file_content):
            if not isinstance(item, dict):
                raise exc.ValidationError(f"The record {index+1} is not a dictionary.")
            self.validate_against_schema(item, self.schema)
        return True


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