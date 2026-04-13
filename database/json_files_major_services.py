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

It is designed to keep file operations consistent, safe, and schema-compliant across the system.
"""

import json
from datetime import datetime
from pathlib import Path

import database.database_schemes as schemas
import exceptions as exc
import utils.config as config


class JsonFilesService:
    """Service to handle JSON file operations.
    Args:
        file_path (Path): Path to the JSON file.
        schema (dict): Schema used to validate the JSON file structure and field types.
    """

    def __init__(self, file_path: Path, schema: dict | None = None):
        self.file_path = file_path
        self.schema = schema

    # -------------------------
    # File I/O helpers
    # -------------------------

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

    def write_json_data(self, data):
        """Overwrite the file with the provided data after validation.

        Args:
            data (list): Data to persist.

        Raises:
            exc.FileError: If data is empty or not a list.
            exc.ValidationError: If data does not match the schema.
        """
        if data is None:
            raise exc.FileError("Data is empty. Cannot save empty data to the file.")
        if not isinstance(data, list):
            raise exc.FileError("Data is not a list. Cannot save data to the file.")

        for record in data:
            self.validate_against_schema(record, self.schema)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4, sort_keys=True)

        return "Success. Data have been saved in the file."

    # -------------------------
    # CRUD operations
    # -------------------------

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
        if data_to_append is None:
            raise exc.ValidationError("New data is missig or it's an empty value.")

        if not isinstance(data_to_append, dict):
            raise exc.ValidationError(
                "Incorrect type of data to append. Cannot add data to database, expected type of data is dict."
            )

        validated_record = self.validate_against_schema(data_to_append, self.schema)
        current_data.append(validated_record)
        self.write_json_data(current_data)
        return f"Success. Data had been added and saved to file: {self.file_path.name}"

    # -------------------------
    # Core validation
    # -------------------------

    def validate_against_schema(self, data, schema, path=""):
        """Recursively validate value types against a given schema.

        Args:
            data: The data to validate.
            schema: The schema to validate against.

        Returns:
            data: The validated data if it matches the schema.

        Raises:
            exc.ValidationError: If given data is None, schema is empty or data has wrong type.
        """

        error_location = f"at '{path}'" if path else ""

        if not schema:
            raise exc.ValidationError(
                f"Given schema is empty. Cannot validate against empty schema {error_location}"
            )

        if data is None:
            # In some cases None value is acceptable in some optional fields.
            if schema is type(None):
                return data
            if isinstance(schema, tuple) and type(None) in schema:
                return data
            raise exc.ValidationError(
                f"Data to validate is missing or it's an empty value {error_location}"
            )

        if isinstance(schema, tuple):
            if schema and schema[0] == "one_of":
                valid_values = schema[1]
                if data not in valid_values:
                    raise exc.ValidationError(
                        f"Provided value of the field is not valid {error_location}"
                    )
                return data

            elif schema and schema[0] != "one_of":
                for option in schema:
                    try:
                        self.validate_against_schema(data, option, path)
                        return data
                    except exc.ValidationError:
                        continue
                raise exc.ValidationError(
                    f"Provided value does not match any of the options in the schema {error_location}"
                )

        if isinstance(schema, dict):
            if not isinstance(data, dict):
                raise exc.ValidationError(
                    f"Provided data has wrong type. Expected data type is dict {error_location}"
                )

            if "fields" in schema:
                fields = schema.get("fields", {})
                required = schema.get("required", [])

                for key in required:
                    missing_path = f"{path}.{key}" if path else key
                    if key not in data:
                        raise exc.ValidationError(
                            f"Required key is missing: {missing_path}"
                        )

                for key, subschema in fields.items():
                    child_path = f"{path}.{key}" if path else key
                    if key in data:
                        self.validate_against_schema(data[key], subschema, child_path)
                return data
            raise exc.ValidationError(
                f"Format of the schema is invalid {error_location}. Expected schema is a dict with 'fields' and 'required' keys."
            )

        if isinstance(schema, str):
            if schema == "date":
                if not isinstance(data, str):
                    raise exc.ValidationError(
                        f"Invalid type of date {error_location}. Expected date format is a string: YYYY-MM-DD"
                    )

                try:
                    datetime.strptime(data, "%Y-%m-%d")
                except ValueError:
                    raise exc.ValidationError(
                        f"Invalid date format {error_location}. Expected format is YYYY-MM-DD"
                    )
                return data

            if schema == "datetime":
                if not isinstance(data, str):
                    raise exc.ValidationError(
                        f"Invalid type for datetime {error_location}. Expected type is datetime string."
                    )

                try:
                    datetime.fromisoformat(data)
                except ValueError:
                    raise exc.ValidationError(
                        f"Invalid datetime format {error_location}. Expected ISO format"
                    )

                return data

            raise exc.ValidationError(
                f"Unsupported string schema {error_location}: {schema}"
            )

        if isinstance(schema, type):
            if not isinstance(data, schema):
                raise exc.ValidationError(
                    f"Wrong type of data {error_location}. Expected {schema.__name__}, got {type(data).__name__}."
                )
            else:
                return data

        raise exc.ValidationError(f"Unsupported schema type {error_location}: {schema}")

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

        if not isinstance(file_content, list):
            raise exc.ValidationError("File must contain a list of records")

        for index, item in enumerate(file_content):
            if not isinstance(item, dict):
                raise exc.ValidationError(f"The record {index+1} is not a dictionary.")

            try:
                self.validate_against_schema(item, self.schema)
            except exc.ValidationError as e:
                raise exc.ValidationError(
                    f"Validation failed for record {index + 1}: {e}"
                )

        return True

    # -------------------------
    # Backup helpers
    # -------------------------

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
            str: Backup filename. Example: "library_copy_users_2024-06-01_12-00-00.json"
        """
        alias = config.PROJECT_ALIAS
        name = self.file_path.stem
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"

        return backup_file_name

    def create_backup_file(self):
        """Create a JSON backup with a timestamped filename in the backup directory.

        Returns:
            Path : Confirmation that backup has been created, including the target path.
        """
        self.file_exists_checking()
        backup_dir = self.get_or_create_backup_dir()
        backup_file_name = self.build_backup_file_name()
        backup_path = backup_dir / backup_file_name
        data = self.load_json_file()

        with backup_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4, sort_keys=True)
        return backup_path

    # -------------------------
    # Remove/Update operations
    # -------------------------

    def remove_from_file(self, key_name, key_value):
        """Remove records matching a key/value pair.

        TO DO: Implement recursive existence checks (for supporting nested keys)

        Args:
            key_name (str): Field name to match.
            key_value: Value to match for removal.

        Raises:
            exc.DatabaseError: If no matching records are found.
        """
        file_content = self.load_json_file()
        records_to_remove = []
        records_to_delete_counter = 0

        if key_name is None:
            raise exc.ValidationError("Key name is missing or it's an empty value.")

        if key_value is None:
            raise exc.ValidationError("Key value is missing or it's an empty value.")

        if not key_name in self.schema:
            raise exc.InvalidFieldError(
                f"The key: {key_name} is not present in file schema."
            )

        for record in file_content:
            if not isinstance(record, dict):
                raise exc.ValidationError(
                    "Incorrect type of record data. Expected type is dict."
                )
            elif key_name in record and record[key_name] == key_value:
                records_to_remove.append(record)
                records_to_delete_counter += 1

        if records_to_delete_counter == 0:
            raise exc.DatabaseError(
                f"No matching elements to key {key_name} and value {key_value}. No data deleted."
            )

        for record in records_to_remove:
            file_content.remove(record)

        self.write_json_data(file_content)
        return f"Success. Data from the file deleted for record: {key_name}"

    def update_data_in_file(self, item, new_data, match_key, match_value):
        """Update a field in all records where it exists.

        Args:
            item (str): Field name to update.
            new_data (str): New value for the field.
            match_key (str) : Name of the field used to find the record to update.
            match_value : Value used to select one record to update

        Raises:
            exc.FileError: If the new value is empty.
            exc.DatabaseError: If no matching field is found.
        """
        file_content = self.load_json_file()
        updated = 0

        if item is None:
            raise exc.FileError("Item to update can't be empty value.")

        if not item in self.schema:
            raise exc.InvalidFieldError(
                f"The field {item} is not present in file schema."
            )

        if new_data is None:
            raise exc.ValidationError("New data is missing or it's an empty value.")

        for record in file_content:
            if not isinstance(record, dict):
                raise exc.ValidationError(
                    "Incorrect type of record data. Expected type is dict."
                )
            elif record.get(match_key) == match_value:
                record[item] = new_data
                updated += 1
                break

        if updated == 0:
            raise exc.DatabaseError(
                f"No matching element to where {match_key} == {match_value}."
            )

        self.write_json_data(file_content)

        return "Success. Record in database has been updated."


# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database
