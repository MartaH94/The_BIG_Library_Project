"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

TO DO HERE:
- Create unit tests for all methods in json_files_major_services module. method by method.

Test cases should cover behaviors for all methods, including edge cases and error handling.


Test classes: 11
Test cases total: 45


TO DO:
Implement all planned tests

"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase

import exceptions as exc
import utils.config as config
from database.json_files_major_services import JsonFilesService
from models.user import User
from services.authorisation_service import UserAuthorisation


# -------------------------
# File I/O helpers | Test cases: to do: 12
# -------------------------
class TestMethodFileExistsChecking(unittest.TestCase):  # 4/4
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
        self.json_service = JsonFilesService(file_path=self.path_to_non_existent_file)
        file_to_check = self.path_to_non_existent_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertIsInstance(file_content, list)

    def test_initializes_list_in_empty_file(self):
        self.json_service = JsonFilesService(file_path=self.path_to_empty_file)
        file_to_check = self.path_to_empty_file
        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, [])

    def test_no_action_when_file_has_content(self):
        self.json_service = JsonFilesService(file_path=self.path_to_file_with_content)
        file_to_check = self.path_to_file_with_content

        with open(file_to_check, encoding="utf-8") as f:
            before_content = json.load(f)

        self.json_service.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            after_content = json.load(f)

        self.assertEqual(before_content, after_content)


class TestMethodLoadJsonFile(unittest.TestCase):  # 4
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

        """ load_json_file expects a list in valid JSON file """
        self.valid_file_data = [
            {"service": "loan", "enabled": True},
            {"user_id": 112233, "enabled": True},
        ]

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_creates_missing_file_and_returns_empty_list(self):
        pass

    def test_reads_existing_list_from_file(self):
        self.valid_json_file = self.valid_json_file_path

        with self.valid_json_file.open("w", encoding="utf-8") as f:
            json.dump(self.valid_file_data, f)

        self.load_service.file_path = self.valid_json_file_path

        test_result = self.load_service.load_json_file()

        self.assertEqual(test_result, self.valid_file_data)

    def test_raises_file_error_if_json_doesnt_contain_list(self):
        pass

    def test_raises_file_error_for_invalid_json_file(self):
        pass


class TestMethodWriteJsonData(unittest.TestCase):  # 4
    def test_raises_file_error_if_data_is_none(self):
        pass

    def test_raises_file_error_if_data_is_not_list(self):
        pass

    def test_writes_valid_list_to_file(self):
        pass

    def test_raises_validation_error_for_invalid_record(self):
        pass


# -------------------------
# CRUD operations | Test cases: to do: 4
# -------------------------


class TestMethodAppendDataToFile(unittest.TestCase):  # 4
    def test_raises_validation_error_if_data_is_none(self):
        pass

    def test_raises_validation_error_if_data_is_not_dict(self):
        pass

    def test_appends_valid_record_to_file(self):
        pass

    def test_raises_validation_error_for_invalid_record(self):
        pass


# -------------------------
# Core validation | Test cases: to do: 10
# -------------------------


class TestMethodValidateAgainstSchema(unittest.TestCase):  # 6
    def test_raises_validation_error_if_data_is_none(self):
        pass

    def test_raises_validation_error_if_schema_is_empty(self):
        pass

    def test_raises_validation_error_if_data_is_not_dict(self):
        pass

    def test_raises_validation_error_if_required_key_is_missing(self):
        pass

    def test_raises_validation_error_if_field_type_is_wrong(self):
        pass

    def test_returns_data_if_schema_matches(self):
        pass


class TestMethodValidateFileData(unittest.TestCase):  # 4
    def test_raises_validation_error_if_file_is_empty(self):
        pass

    def test_raises_validation_error_if_record_is_not_dict(self):
        pass

    def test_raises_validation_error_if_record_does_not_match_schema(self):
        pass

    def test_returns_true_if_all_records_are_valid(self):
        pass


# -------------------------
# Backup helpers | Test cases: to do: 9
# -------------------------


class TestMethodGetOrCreateBackupDir(unittest.TestCase):  # 2

    def test_creates_backup_directory_if_missing(self):
        pass

    def test_returns_existing_backup_directory(self):
        pass


class TestMethodBuildBackupFileName(unittest.TestCase):  # 3
    def test_backup_name_has_correct_name(self):
        pass

    def test_backup_name_contains_timestamp(self):
        pass

    def test_backup_name_has_json_extension(self):
        pass


class TestMethodCreateBackupFile(unittest.TestCase):  # 4
    def test_creates_backup_file_and_returns_path(self):
        pass

    def test_backup_file_contains_same_data_as_source_file(self):
        pass

    def test_creates_backup_directory_if_missing(self):
        pass

    def test_backup_file_name_contains_alias_stem_and_timestamp(self):
        pass


# -------------------------
# Remove/Update operations | Test cases: to do: 10
# -------------------------


class TestMethodRemoveFromFile(unittest.TestCase):  # 5
    def test_raises_validation_error_if_key_name_is_none(self):
        pass

    def test_raises_validation_error_if_key_value_is_none(self):
        pass

    def test_raises_invalid_field_error_if_key_not_in_schema(self):
        pass

    def test_raises_database_error_if_no_matching_record_found(self):
        pass

    def test_removes_matching_records_and_saves_file(self):
        pass


class TestMethodUpdateDataInFile(unittest.TestCase):  # 5
    def test_raises_file_error_if_item_is_none(self):
        pass

    def test_raises_invalid_field_error_if_item_not_in_schema(self):
        pass

    def test_raises_validation_error_if_new_data_is_none(self):
        pass

    def test_raises_database_error_if_item_not_found_in_records(self):
        pass

    def test_updates_existing_field_and_saves_file(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
