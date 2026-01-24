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
    """ Service to handle JSON file operations.
    Args:
        file_path (Path): Path to the JSON file.
        schema (dict): Schema to validate the JSON file structure and fields.
    """

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
        

    def load_json_file(self):   
        """Read JSON file content. 
        Returns: list - Content of the JSON file as a list of items."""
        self.file_exists_checking()
        
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise exc.FileError("File should be a list of items. Check file structure.")
                return data
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read the file: {e} from program data directory.")
        
        return data
        
        
    def write_json_data(self, data):
        """ Write data to the JSON file.
            Args: data (list) - Data to write to the JSON file. 
        """
        if not data:
            raise exc.FileError("Data is empty. Cannot save empty data to the file.")
        if not isinstance(data, list):
            raise exc.FileError("Data is not a list. Cannot save data to the file.") 
        self.validate_against_schema(data,[self.schema])       
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)

        return "Success. Changes has been saved."


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
        return f"Success. Data had been added and saved to file: {self.file_path.name}"
      


    def validate_against_schema(self, data, schema):
        """The method to validate values type and structure against the given schema. 
        Args:
            data: The data to validate.
            schema: The schema to validate against.
        """
        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise exc.ValidationError(f"Given value {data} should be a dictionary")
            for key, subschema in schema.items():
                if key not in data:
                    raise exc.ValidationError(f"Missing key {key} in {subschema}")
                self.validate_against_schema(data[key], subschema)
        else:
            if not isinstance(data, schema):
                raise exc.ValidationError("Wrong type of data. Expected dict.")
            
        return "Success. Data has been validated and matches the file schema."


    def validate_file_data(self): 
        """ Veryfying if the list of items in the JSON file is not empty and each item matches the expected schema.
        Returns: bool - True if all items in the file match the schema; raises ValidationError otherwise.
        """
        self.file_exists_checking()
        file_content = self.load_json_file()

        if not file_content:
            raise exc.ValidationError(f"File {self.file_path.name} is empty. Cannot validate fields in an empty file.")  
        for index, item in enumerate(file_content):
            if not isinstance(item, dict):
                raise exc.ValidationError(f"The record {index+1} is not a dictionary.")
            self.validate_against_schema(item, self.schema)
        return True



    def get_or_create_backup_dir(self):
        """ Get or create the backup directory for the JSON file.
        Returns: Path - The path to the backup directory.
        """
        name = self.file_path.stem
        backup_dir = config.BACKUP_FILES_DIRECTORY/ name 
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def build_backup_file_name(self):
        """ Build a timestamped backup file name for the JSON file.
        Returns: str - The backup file name.
        """
        alias = config.PROJECT_ALIAS 
        name = self.file_path.stem 
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"
        
        return backup_file_name

    def create_backup_file(self):
        """ Create a backup of the current JSON file with a timestamped filename in the backup directory.
        Returns: Path - The path to the created backup file.
        """
        self.file_exists_checking()
        backup_dir = self.get_or_create_backup_dir()
        backup_file_name = self.build_backup_file_name()
        backup_path = backup_dir/backup_file_name
        data = self.load_json_file()
            
        with backup_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4, sort_keys=True)
        return "Success. Backup file has been created."



    def remove_from_file(self, key_name, key_value):
        """The method to remove records from the JSON file based on a specific key-value pair.
        Args:
            key_name (str): The key name to search for in the records.
            key_value: The value associated with the key to identify records to be removed.
        """
        file_content = self.load_json_file()
        records_to_remove = []
        deleted_records_counter = 0

        for record_id, record_data in file_content.items():
            if key_name in record_data and record_data[key_name] == key_value:            
                records_to_remove.append(record_id)
                deleted_records_counter += 1

        if deleted_records_counter == 0:
            raise exc.DatabaseError(f"No matching elements to key {key_name} and value {key_value}")
        
        for record_id in records_to_remove:
            del file_content[record_id]

        self.validate_file_data(file_content)
        self.write_json_data(file_content)
        return f"Success. Data from the file deleted for record: {key_name}"

  
    def update_data_in_file(self, item, new_data): 
        """ Update an existing item in the JSON file with new data.
        Args:
            item (str): The existing item (field) to update.
            new_data (str): The new data to update the item with.
        """
        file_content = self.load_json_file()    
        updated = 0
        if not new_data:
            raise exc.FileError(f"New data can't be empty value.")
        for record_id, record_data in file_content.items():
            if item in record_data:
                record_data[item] = new_data
                updated += 1
        if updated == 0:
            raise exc.DatabaseError(f"No matching element to {item}.")
        
        self.validate_file_data(file_content)
        self.write_json_data(file_content)

        return "Success. Record in database has been updated."






        

# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database