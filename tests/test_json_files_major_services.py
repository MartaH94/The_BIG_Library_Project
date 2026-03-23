"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

TO DO HERE:
- Create unit tests for all methods in json_files_major_services module. method by method.

Test cases should cover behaviors for all methods, including edge cases and error handling.




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
# File I/O helpers
# -------------------------
class TestMethodFileExistsChecking(unittest.TestCase):
    def test_creates_file_when_missing(self):
        pass

    def test_initializes_empty_file(self):
        pass

    def test_no_action_when_file_has_content(self):
        pass


class TestMethodLoadJsonFile(unittest.TestCase):
    def test_creates_missing_file_and_returns_empty_list(self):
        pass

    def test_reads_existing_list_from_file(self):
        pass

    def test_raises_file_error_if_json_doesnt_contain_list(self):
        pass

    def test_raises_file_error_for_invalid_json_file(self):
        pass


class TestMethodWriteJsonData(unittest.TestCase):
    def test_raises_file_error_if_data_is_none(self):
        pass

    def test_raises_file_error_if_data_is_not_list(self):
        pass

    def test_writes_valid_list_to_file(self):
        pass

    def test_raises_validation_error_for_invalid_record(self):
        pass

# -------------------------
# CRUD operations
# -------------------------


class TestMethodAppendDataToFile(unittest.TestCase):
    def test_raises_validation_error_if_data_is_none(self):
        pass

    def test_raises_validation_error_if_data_is_not_dict(self):
        pass

    def test_appends_valid_record_to_file(self):
        pass

    def test_raises_validation_error_for_invalid_record(self):
        pass

# -------------------------
# Core validation
# -------------------------


class TestMethodValidateAgainstSchema(unittest.TestCase):
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


class TestMethodValidateFileData(unittest.TestCase):
    def test_raises_validation_error_if_file_is_empty(self):
        pass

    def test_raises_validation_error_if_record_is_not_dict(self):
        pass

    def test_raises_validation_error_if_record_does_not_match_schema(self):
        pass

    def test_returns_true_if_all_records_are_valid(self):
        pass


# -------------------------
# Backup helpers
# -------------------------


class TestMethodGetOrCreateBackupDir(unittest.TestCase):

    def test_creates_backup_directory_if_missing(self):
        pass

    def test_returns_existing_backup_directory(self):
        pass


class TestMethodBuildBackupFileName(unittest.TestCase):
    def test_backup_name_has_correct_name(self):
        pass

    def test_backup_name_contains_timestamp(self):
        pass

    def test_backup_name_has_json_extension(self):
        pass


class TestMethodCreateBackupFile(unittest.TestCase):
    def test_creates_backup_file_and_returns_path(self):
        pass

    def test_backup_file_contains_same_data_as_source_file(self):
        pass

    def test_creates_backup_directory_if_missing(self):
        pass

    def test_backup_file_name_contains_alias_stem_and_timestamp(self):
        pass


# -------------------------
# Remove/Update operations
# -------------------------


class TestMethodRemoveFromFile(unittest.TestCase):
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


class TestMethodUpdateDataInFile(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
