"""
__________________________________________________________
database.json_files_major_services.py
==========================================================
Database service for JSON files.
__________________________________________________________


Utility service for managing JSON-based data storage in the project.
This module provides a high-level interface for working with JSON files, including:
- loading and saving data,
- validating records against a defined schema,
- appending and updating entries,
- removing records by key/value,
- and generating timestamped backups.

It is designed to keep file operations consistent, safe, and schema‑compliant across the system.


"""

import json
from datetime import datetime
from pathlib import Path

import exceptions as exc
import utils.config as config
from database import database_schemes


class JsonFilesService:
    """Service to handle JSON file operations.
    Args:
        file_path (Path): Path to the JSON file.
        schema (dict): Schema used to validate the JSON file structure and field types.
    """

    def __init__(self, file_path: Path, schema: dict):
        self.file_path = file_path
        self.schema = schema

    def file_exists_checking(self):
        """Ensure the JSON file exists and is initialized. If the file is missing or empty, it is created with an empty list.

        Returns:
            str: Status message about the verification/creation.
        """
        if not self.file_path.exists():
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump([], f, indent=4, sort_keys=True)
                return "File didn't exist. Created new file with empty list."

        if self.file_path.stat().st_size == 0:
            with self.file_path.open("w", encoding="utf-8") as f:
                json.dump([], f, indent=4, sort_keys=True)
                return "File was empty. Created new file with empty list."

    def load_json_file(self):
        """Load and return the JSON file content.

        Returns:
            list: Parsed JSON content.

        Raises:
            exc.FileError: If content is not a list or JSON cannot be decoded.
        """
        self.file_exists_checking()

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise exc.FileError(
                        "File should be a list of items. Check file structure."
                    )
                return data
        except json.JSONDecodeError as e:
            raise exc.FileError(
                f"Cannot read the file: {e} from program data directory."
            )

        return data

    def write_json_data(self, data):
        """Overwrite the file with the provided data after validation.

        Args:
            data (list): Data to persist.

        Raises:
            exc.FileError: If data is empty or not a list.
            exc.ValidationError: If data does not match the schema.
        """
        if not data:
            raise exc.FileError("Data is empty. Cannot save empty data to the file.")
        if not isinstance(data, list):
            raise exc.FileError("Data is not a list. Cannot save data to the file.")

        for record in data:
            self.validate_against_schema(record, self.schema)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, sort_keys=True)

        return "Success. Data have been saved in the file."

    def append_data_to_file(self, data_to_append):
        """Append a new record to the JSON file.

        Args:
            data_to_append (dict): A single record to add (e.g., new user or book).

        Returns:
            str: Confirmation message.

        Raises:
            exc.ValidationError: If the record is empty or invalid.
        """
        current_data = self.load_json_file()
        if not data_to_append:
            raise exc.ValidationError(
                "New record is empty. Cannot save dictionary to the file."
            )

        self.validate_against_schema(data_to_append, self.schema)
        current_data.append(data_to_append)
        self.write_json_data(current_data)
        return f"Success. Data had been added and saved to file: {self.file_path.name}"

    def validate_against_schema(self, data, schema):
        """Recursively validate value types against a given schema.

        Args:
            data: The data to validate.
            schema: The schema to validate against.

        Returns:
            str - Confirmation message (If data matches the schema)

        Raises:
            exc.ValidationError: If given data is None, schema is empty or data has wrong type.
        """
        if data is None:
            raise exc.ValidationError("Given value is None. Cannot validate NoneType.")

        if not schema:
            raise exc.ValidationError(
                "Given schema is empty. Cannot validate against empty schema."
            )

        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise exc.ValidationError(
                    "Provided data has wrong type. Expected data type is dict."
                )

            for key, subschema in schema.items():
                if key not in data:
                    raise exc.ValidationError(f"Missing key {key}")
                self.validate_against_schema(data[key], subschema)
            return "Success. Data is dictionary and matches the schema."

        if isinstance(schema, type):
            if not isinstance(data, schema):
                raise exc.ValidationError(
                    f"Wrong type of data. Expected {schema.__name__}, got {type(data).__name__}."
                )
            else:
                return "Success. Data type matches the schema type."

    def validate_file_data(self):
        """Validate all records loaded  from JSON file against the service schema.

        This method loads the JSON file content, ensures it is a non-empty list of dictionary records, and validates each record using the configured schema via validate_against_schema().
        A ValidationError is raised if the file is empty, a record is not a dictionary, or any record fails schema validation. Returns True if all records are valid.

        Returns:
            bool - True if validation passes (All items in the file match the schema)

        Raises:
            exc.ValidationError: If keys are missing or types do not match.
        """
        self.file_exists_checking()
        file_content = self.load_json_file()

        if not file_content:
            raise exc.ValidationError(
                f"File {self.file_path.name} is empty. Cannot validate fields in an empty file."
            )
        for index, item in enumerate(file_content):
            if not isinstance(item, dict):
                raise exc.ValidationError(f"The record {index+1} is not a dictionary.")
            self.validate_against_schema(item, self.schema)
        return True

    def get_or_create_backup_dir(self):
        """Return the directory where backups are stored, creating it if needed.

        Returns:
            Path: Backup directory path.
        """
        name = self.file_path.stem
        backup_dir = config.BACKUP_FILES_DIRECTORY / name
        if not backup_dir.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
        return backup_dir

    def build_backup_file_name(self):
        """Build a timestamped backup filename based on project alias and file name.

        Returns:
            str: Backup filename.
        """
        alias = config.PROJECT_ALIAS
        name = self.file_path.stem
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"

        return backup_file_name

    def create_backup_file(self):
        """Create a JSON backup with a timestamped filename in the backup directory.

        Returns:
            str: Confirmation that backup has been created, including the target path.
        """
        self.file_exists_checking()
        backup_dir = self.get_or_create_backup_dir()
        backup_file_name = self.build_backup_file_name()
        backup_path = backup_dir / backup_file_name
        data = self.load_json_file()

        with backup_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4, sort_keys=True)
        return backup_path

    def remove_from_file(self, key_name, key_value):
        """Remove records matching a key/value pair.

        Args:
            key_name (str): Field name to match.
            key_value: Value to match for removal.

        Raises:
            exc.DatabaseError: If no matching records are found.
        """
        file_content = self.load_json_file()
        records_to_remove = []
        records_to_delete_counter = 0

        if key_name == None or key_value == None:
            raise exc.FileError("Key name or key value can't be empty.")

        for record_id, record_data in enumerate(file_content):
            if not isinstance(record_data, dict):
                raise exc.ValidationError(
                    "Incorrect type of record data. Expected type is dict."
                )
            elif key_name in record_data and record_data[key_name] == key_value:
                records_to_remove.append(record_id)
                records_to_delete_counter += 1

        if records_to_delete_counter == 0:
            raise exc.DatabaseError(
                f"No matching elements to key {key_name} and value {key_value}"
            )

        sorted_records_to_remove = records_to_remove.sort(reverse=True)

        for record_id in sorted_records_to_remove:
            if record_id < len(file_content):
                del file_content[record_id]

        self.validate_file_data()
        self.write_json_data(file_content)
        return f"Success. Data from the file deleted for record: {key_name}"

    def update_data_in_file(self, item, new_data):
        """Update a field in all records where it exists.

        Args:
            item (str): Field name to update.
            new_data (str): New value for the field.

        Raises:
            exc.FileError: If the new value is empty.
            exc.DatabaseError: If no matching field is found.
        """
        file_content = self.load_json_file()
        updated = 0

        if item == None:
            raise exc.FileError("Item to update can't be empty value.")

        if new_data == None:
            raise exc.FileError(f"New data can't be empty value.")

        for record in enumerate(file_content):
            if not isinstance(record, dict):
                raise exc.ValidationError(
                    "Incorrect type of record data. Expected type is dict."
                )
            elif item in record:
                record[item] = new_data
                updated += 1

        if updated == 0:
            raise exc.DatabaseError(f"No matching element to {item}.")

        self.validate_file_data()
        self.write_json_data(file_content)

        return "Success. Record in database has been updated."


# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database
