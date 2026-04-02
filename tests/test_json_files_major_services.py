"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

Test classes: 11
Test cases total: 44

current status: in progress
Total number of done test cases: 11/44

"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
import utils.config as config
from database.json_files_major_services import JsonFilesService
from models.user import User
from services.authorisation_service import UserAuthorisation


# -------------------------
# File I/O helpers | Test cases: to do: 11
# -------------------------
class TestMethodFileExistsChecking(unittest.TestCase):  # 3/3
    """Method under test: file_exists_checking
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

        self.path_to_non_existent_file = (
            Path(self.temporary_dir.name) / "non_existent_file.json"
        )

        self.path_to_empty_file = Path(self.temporary_dir.name) / "empty_file.json"

        self.path_to_empty_file.write_text("", encoding="utf-8")

        self.path_to_file_with_content = (
            Path(self.temporary_dir.name) / "file_with_content.json"
        )

        self.path_to_file_with_content.write_text("[]", encoding="utf-8")

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_file_when_missing(self):
        """expected behavior: file_exists_checking creates a new file if it doesn't exist and initializes it with an empty list as JSON content"""
        self.json_service = JsonFilesService(file_path=self.path_to_non_existent_file)
        file_to_check = self.path_to_non_existent_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertIsInstance(file_content, list)

    def test_initializes_list_in_empty_file(self):
        """expected behavior: file_exists_checking initializes an empty file with an empty list as JSON content"""
        self.json_service = JsonFilesService(file_path=self.path_to_empty_file)
        file_to_check = self.path_to_empty_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, [])

    def test_no_action_when_file_has_content(self):
        """expected behavior: file_exists_checking does not modify the file if it already has content. The content of the file remains unchanged after the method is called"""
        self.json_service = JsonFilesService(file_path=self.path_to_file_with_content)
        file_to_check = self.path_to_file_with_content

        with open(file_to_check, encoding="utf-8") as f:
            before_content = json.load(f)

        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            after_content = json.load(f)

        self.assertEqual(before_content, after_content)


class TestMethodLoadJsonFile(unittest.TestCase):  # 4/4
    """Method under test: load_json_file
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        """ Paths to test files """
        self.valid_json_file_path = self.temporary_dir_path / "valid_file.json"
        self.invalid_json_file_path = self.temporary_dir_path / "invalid_file.json"
        self.empty_json_file_path = self.temporary_dir_path / "empty_file.json"
        self.missing_json_file_path = self.temporary_dir_path / "missing_file.json"

        """ Service under test """
        self.load_service = JsonFilesService(file_path=self.valid_json_file_path)

        """ Test data
        load_json_file expects a list in valid JSON file """
        self.valid_file_data = [
            {"service": "loan", "enabled": True},
            {"user_id": 112233, "enabled": True},
        ]
        self.invalid_file_data = {"book_id": 212121, "enabled": False}

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_reads_existing_list_from_file(self):
        with self.valid_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_file_data, f)

        self.load_service.file_path = self.valid_json_file_path
        test_result = self.load_service.load_json_file()
        self.assertEqual(test_result, self.valid_file_data)

    def test_returns_empty_list_when_json_file_is_empty(self):
        """expected behavior: json_load_file returns an JSON content as an empty list in case file to load is empty"""
        with self.empty_json_file_path.open("w", encoding="utf-8"):
            pass

        self.load_service.file_path = self.empty_json_file_path
        test_result = self.load_service.load_json_file()
        self.assertEqual(test_result, [])

    def test_raises_error_when_json_file_is_invalid(self):
        """expected behavior: json.JSONDecodeError is caught and exc.FileError is raised in case JSON file is corrupted"""
        self.invalid_json_file_path.write_text(
            '{"book_id": 212121, "enabled": False"', encoding="utf-8"
        )

        self.load_service.file_path = self.invalid_json_file_path
        with self.assertRaises(exc.FileError) as cm:
            self.load_service.load_json_file()

        self.assertIn("Cannot read the file", str(cm.exception))

    def test_raises_error_when_json_file_type_is_not_list(self):
        """expected behavior: raising exc.FileError when JSON file doesn't consist of list of items and has incorrect data type"""
        with self.invalid_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.invalid_file_data, f)

        self.load_service.file_path = self.invalid_json_file_path

        with self.assertRaises(
            exc.FileError
        ) as cm:  # cm stands for: context manager result (the captured exception)
            self.load_service.load_json_file()

        self.assertIn("File should be a list", str(cm.exception))


class TestMethodWriteJsonData(unittest.TestCase):  # 4/4
    """Method under test: write_json_data
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        """ Path to test file. We need this file to have a file to write data in it.
        Also preparing test file"""
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"
        self.test_json_file_path.write_text("[]", encoding="utf-8")

        """ valid data must match schema and validator expectations"""
        self.schema = {"service": str, "enabled": bool}
        self.valid_data = [
            {"service": "loan", "enabled": True},
            {"user_id": 112233, "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_data, f, ensure_ascii=True, indent=4, sort_keys=True)

        """ Service under test """
        self.write_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_file_error_if_data_is_none(self):
        """expected behavior: Raises exc.FileError in case the data to save in file is missing or it's an empty value"""
        self.data_to_write = None
        with self.assertRaises(exc.FileError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Cannot save empty data", str(cm.exception))

    def test_raises_file_error_if_data_is_not_list(self):
        """expected behavior: Raises exc.FileError in case the data to save in file is not a type of list"""
        self.data_to_write = {"book_id": 123321, "enabled": True}
        with self.assertRaises(exc.FileError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Data is not a list", str(cm.exception))

    def test_writes_valid_list_to_file(self):
        """expected behavior: Data is correct and is saved in JSON file. Return message with confirmation is displayed"""
        self.data_to_write = [{"service": "loan", "enabled": True}]
        test_result = self.write_service.write_json_data(self.data_to_write)

        self.assertEqual(test_result, "Success. Data have been saved in the file.")
        self.assertTrue(self.test_json_file_path.exists())

        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, self.data_to_write)

    def test_raises_validation_error_for_invalid_record(self):
        """expected behavior: Raises exc.ValidationError in case the data doesn't match schema"""
        self.data_to_write = ["service", "loan", "enabled=True"]
        with self.assertRaises(exc.ValidationError) as cm:
            self.write_service.write_json_data(self.data_to_write)
        self.assertIn("Expected data type is dict", str(cm.exception))


# -------------------------
# CRUD operations | Test cases: to do: 4
# -------------------------


class TestMethodAppendDataToFile(unittest.TestCase):  # 4/4
    """Method under test: append_data_to_file
    Number of TestCases: 4
    Done TestCases: 4
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        """ valid data must match schema and validator expectations"""
        self.valid_data = [
            {"service": "loan", "enabled": True},
            {"service": "return", "enabled": True},
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_data, f, ensure_ascii=True, indent=4, sort_keys=True)

        self.data_to_append = {"service": "reservation", "enabled": False}

        """ Service under test """
        self.append_data_service = JsonFilesService(
            file_path=self.test_json_file_path, schema={"service": str, "enabled": bool}
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the data to append in file is missing or it's an empty value"""
        self.data_to_append = None
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("New data is missig or it's an empty value.", str(cm.exception))

    def test_raises_validation_error_if_data_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the data to append in file is not a type of dict"""
        self.data_to_append = ["service", "reservation", "enabled=False"]
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("Incorrect type of data to append", str(cm.exception))

    def test_appends_valid_record_to_file(self):
        """expected behavior: Data is correct and is appended to JSON file. Return message with confirmation is displayed"""
        self.append_data_service.append_data_to_file(self.data_to_append)
        with self.test_json_file_path.open("r", encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertIn(self.data_to_append, file_content)

    def test_raises_validation_error_for_invalid_record(self):
        """expected behavior: Raises exc.ValidationError in case the data doesn't match schema"""
        self.data_to_append = {"user_id": 123321, "enabled": True}
        with self.assertRaises(exc.ValidationError) as cm:
            self.append_data_service.append_data_to_file(self.data_to_append)

        self.assertIn("Missing key", str(cm.exception))


# -------------------------
# Core validation | Test cases: to do: 10
# -------------------------


class TestMethodValidateAgainstSchema(unittest.TestCase):  # _/6
    """Method under test: validate_against_schema
    Number of TestCases: 6
    Done TestCases: 2
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

        """ file_path is not used by validate_against_schema method, but it's required to create an instance of JsonFilesService, so we need to prepare it"""
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.test_schema = {"service": str, "enabled": bool}

        """ service under test """
        self.validation_service = JsonFilesService(
            file_path=self.test_json_file_path, schema=self.test_schema
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is missing or it's an empty value"""
        self.data_to_validate = None
        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn(
            "Data to validate is missing or it's an empty value.", str(cm.exception)
        )

    def test_raises_validation_error_if_schema_is_empty(self):
        """expected behavior: Raises exc.ValidationError in case the schema to validate against is missing or it's an empty value"""
        self.data_to_validate = {"service": "loan", "enabled": True}
        self.test_schema = ""

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Cannot validate against empty schema.", str(cm.exception))

    def test_raises_validation_error_if_data_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is not a type of dict"""
        self.data_to_validate = ["service", "return", False]

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Provided data has wrong type.", str(cm.exception))

    def test_raises_validation_error_if_required_key_is_missing(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate is missing required key(s) defined in schema"""
        self.data_to_validate = {"user_id": 123321, "enabled": True}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Missing key", str(cm.exception))

    def test_raises_validation_error_if_field_type_is_wrong(self):
        """expected behavior: Raises exc.ValidationError in case the data to validate has wrong data type for field(s) defined in schema"""
        self.data_to_validate = {"service": 123455, "enabled": "True"}

        with self.assertRaises(exc.ValidationError) as cm:
            self.validation_service.validate_against_schema(
                self.data_to_validate, self.test_schema
            )

        self.assertIn("Wrong type of data.", str(cm.exception))

    def test_returns_data_if_schema_matches(self):
        """expected behavior: Returns the data if it matches the schema. No exception is raised."""
        self.data_to_validate = {"service": "reserve", "enabled": True}
        result = self.validation_service.validate_against_schema(
            self.data_to_validate, self.test_schema
        )

        self.assertEqual(result, self.data_to_validate)


class TestMethodValidateFileData(unittest.TestCase):  # 4
    """Method under test: validate_file_data
    Number of TestCases: 4
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_file_is_empty(self):
        """expected behavior: Raises exc.ValidationError in case the file to validate is empty. The file should contain a list of records to be valid."""
        pass

    def test_raises_validation_error_if_record_is_not_dict(self):
        """expected behavior: Raises exc.ValidationError in case the file to validate contains record(s) that are not of type dict. Each record in the file should be a dict to be valid."""
        pass

    def test_raises_validation_error_if_record_does_not_match_schema(self):
        """expected behavior: Raises exc.ValidationError in case the file to validate contains record(s) that do not match the defined schema. Each record in the file should conform to the schema to be valid."""
        pass

    def test_returns_true_if_all_records_are_valid(self):
        """expected behavior: Returns True if all records in the file are valid according to the defined schema. No exception is raised."""
        pass


# -------------------------
# Backup helpers | Test cases: to do: 9
# -------------------------


class TestMethodGetOrCreateBackupDir(unittest.TestCase):  # 2
    """Method under test: get_or_create_backup_dir
    Number of TestCases: 2
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_backup_directory_if_missing(self):
        """expected behavior: get_or_create_backup_dir creates a backup directory if it doesn't exist and returns the path to the created directory. The method should ensure that the backup directory is created successfully and is ready for use."""
        pass

    def test_returns_existing_backup_directory(self):
        """expected behavior: get_or_create_backup_dir returns the path to the existing backup directory if it already exists. The method should recognize that the backup directory is already present and return its path without attempting to create a new one."""
        pass


class TestMethodBuildBackupFileName(unittest.TestCase):  # 3
    """Method under test: build_backup_file_name
    Number of TestCases: 3
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_backup_name_has_correct_name(self):
        """expected behavior: build_backup_file_name generates a backup file name that includes the alias stem and a timestamp. The generated file name should follow the expected format and contain the relevant information to identify the backup."""
        pass

    def test_backup_name_contains_timestamp(self):
        """expected behavior: build_backup_file_name generates a backup file name that includes a timestamp. The generated file name should contain a timestamp that indicates when the backup was created, allowing for easy identification and organization of backup files."""
        pass

    def test_backup_name_has_json_extension(self):
        """expected behavior: build_backup_file_name generates a backup file name that has a .json extension. The generated file name should end with the .json extension, indicating that it is a JSON file and can be easily recognized as such."""
        pass


class TestMethodCreateBackupFile(unittest.TestCase):  # 4
    """Method under test: create_backup_file
    Number of TestCases: 4
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_backup_file_and_returns_path(self):
        """expected behavior: create_backup_file creates a backup file with the correct name and returns the path to the created backup file. The method should successfully create the backup file and provide the correct path for reference."""
        pass

    def test_backup_file_contains_same_data_as_source_file(self):
        """expected behavior: create_backup_file creates a backup file that contains the same data as the source file. The method should ensure that the content of the backup file matches the content of the source file, providing an accurate copy for backup purposes."""
        pass

    def test_creates_backup_directory_if_missing(self):
        """expected behavior: create_backup_file creates a backup directory if it doesn't exist before creating the backup file. The method should ensure that the backup directory is created successfully if it is missing, allowing for proper organization of backup files."""
        pass

    def test_backup_file_name_contains_alias_stem_and_timestamp(self):
        """expected behavior: create_backup_file generates a backup file name that includes the alias stem and a timestamp. The generated file name should follow the expected format and contain the relevant information to identify the backup, including the alias stem and the timestamp."""
        pass


# -------------------------
# Remove/Update operations | Test cases: to do: 10
# -------------------------


class TestMethodRemoveFromFile(unittest.TestCase):  # 5
    """Method under test: remove_from_file
    Number of TestCases: 5
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_if_key_name_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the key name to identify record(s) for removal is missing or it's an empty value. The method should validate the input and ensure that a valid key name is provided for the removal operation."""
        pass

    def test_raises_validation_error_if_key_value_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the key value to identify record(s) for removal is missing or it's an empty value. The method should validate the input and ensure that a valid key value is provided for the removal operation."""
        pass

    def test_raises_invalid_field_error_if_key_not_in_schema(self):
        """expected behavior: Raises exc.InvalidFieldError in case the key name provided for removal is not defined in the schema. The method should validate the key name against the schema and ensure that it is a valid field for identifying records to remove."""
        pass

    def test_raises_database_error_if_no_matching_record_found(self):
        """expected behavior: Raises exc.DatabaseError in case no record matching the provided key name and value is found in the file. The method should search for records based on the provided key and value, and if no matching record is found, it should raise an appropriate error to indicate that the removal operation cannot be performed."""
        pass

    def test_removes_matching_records_and_saves_file(self):
        """expected behavior: Removes all records matching the provided key name and value from the file and saves the updated file. The method should successfully identify and remove the matching records, and then save the changes to the file, ensuring that the file reflects the removal of the specified records."""
        pass


class TestMethodUpdateDataInFile(unittest.TestCase):  # 5
    """Method under test: update_data_in_file
    Number of TestCases: 5
    Done TestCases: 0
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_file_error_if_item_is_none(self):
        """expected behavior: Raises exc.FileError in case the item to update is missing or it's an empty value. The method should validate the input and ensure that a valid item is provided for the update operation."""
        pass

    def test_raises_invalid_field_error_if_item_not_in_schema(self):
        """expected behavior: Raises exc.InvalidFieldError in case the item provided for update contains key(s) that are not defined in the schema. The method should validate the item against the schema and ensure that all fields in the item are valid according to the defined schema."""
        pass

    def test_raises_validation_error_if_new_data_is_none(self):
        """expected behavior: Raises exc.ValidationError in case the new data for update is missing or it's an empty value. The method should validate the input and ensure that valid new data is provided for the update operation."""
        pass

    def test_raises_database_error_if_item_not_found_in_records(self):
        """expected behavior: Raises exc.DatabaseError in case the item provided for update is not found in the existing records in the file. The method should search for the item in the file based on the provided data, and if the item is not found, it should raise an appropriate error to indicate that the update operation cannot be performed."""
        pass

    def test_updates_existing_field_and_saves_file(self):
        """expected behavior: Updates an existing field in the item with new data and saves the updated file. The method should successfully identify the item to update, apply the new data to the existing field, and then save the changes to the file, ensuring that the file reflects the updated information for the specified item."""
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
