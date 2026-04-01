"""
________________________________________________________
tests.test_json_files_service
========================================================
Test Class for json_files_major_services module.
________________________________________________________

This file will be deleted.
"""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase

import database.database_schemes as schemas
import database.json_files_major_services as json_files_major_services
import exceptions as exc
import utils.config as config
from models.user import User
from services.authorisation_service import UserAuthorisation


class TestJsonServices(TestCase):
    def setUp(self):
        self.admin_user = User(
            user_id="Marta.Boss", email="marta@mail.com", role="admin"
        )
        self.admin_authorisation = UserAuthorisation(self.admin_user)
        self.admin_authorisation.login(self.admin_user)

        self.reader_user = User(
            user_id="Andrzej.czytelnik", email="read@andrew.com", role="reader"
        )
        self.reader_authorisation = UserAuthorisation(self.reader_user)
        self.reader_authorisation.login(self.reader_user)

        # self.user_schema = schemas.user_schema
        # self.book_schema = schemas.book_schema
        # self.loan_schema = schemas.loan_schema
        # self.backup_schema = schemas.backup_schema

        self.test_directory = tempfile.TemporaryDirectory()
        self.test_file = Path(self.test_directory.name) / "testing_file.json"
        self.test_file.write_text("[]", encoding="utf-8")
        self.json_services = json_files_major_services.JsonFilesService(
            file_path=self.test_file,
        )

    def tearDown(self):
        self.test_directory.cleanup()

    def test_checking_file_exists(self):  # test ok
        """Test checking if the json file exist. If not, should create a new file with empty list and return status ok."""
        file_to_check = self.json_services.file_path
        self.json_services.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(
            file_content,
            [],
            msg="Checking if the json file exist. If not, should create a new file with empty list and return status ok.",
        )

    def test_load_json_file(self):
        """Test that the file load operation can be performed without errors,verifies the returned data type is a list,
        and ensures the file remains readable after loading.
        """
        result = self.json_services.load_json_file()
        self.assertIsInstance(
            result,
            list,
            msg="The loaded JSON data from load_json_file() should be a list.",
        )

    def test_write_json_data(self):
        self.data_to_write = [{"key": "value"}, {"number": 123}]
        self.saved_data = self.json_services.write_json_data(self.data_to_write)
        self.assertTrue(
            self.saved_data, msg="Data should be written to the JSON file successfully."
        )

    def test_append_data_to_file(self):
        self.data_to_append = {"key": "value"}
        self.adding_data = self.json_services.append_data_to_file(self.data_to_append)
        self.assertTrue(
            self.adding_data,
            msg="New record data should be saved in JSON file successfully.",
        )

    def test_validate_data_against_schema(self):
        self.data = {"key": "value"}
        self.schema_to_validate_against = self.json_services.schema
        self.data_validation = self.json_services.validate_against_schema(
            self.data, self.schema_to_validate_against
        )
        self.assertTrue(
            self.data_validation,
            msg="Data should be validated against schema successfully.",
        )
        pass

    def test_validate_file_data(self):
        """Test that the data in the file is list"""
        data_to_validate = self.json_services.load_json_file()
        self.json_services.validate_file_data()
        self.assertIsInstance(
            data_to_validate,
            dict,
            msg="Validation data against schema should confirm data is a dict.",
        )

    def test_get_or_create_backup_dir(self):
        """Test that the backup directory is created if it does not exist, and that the method returns the correct path to the backup directory."""
        backup_dir = self.json_services.get_or_create_backup_dir()
        self.assertTrue(
            backup_dir.exists(),
            msg="Backup directory should be created if it does not exist.",
        )
        self.assertEqual(
            backup_dir,
            Path(config.BACKUP_FILES_DIRECTORY),
            msg="The method should return the correct path to the backup directory.",
        )

    def test_build_backup_filename(self):
        """Test that backup filename is correctly created."""
        backup_filename = self.json_services.build_backup_file_name()

    def test_create_backup_file(self):
        """Test that the backup file is created."""
        backup_file = self.json_services.create_backup_file()
        self.assertTrue(
            backup_file.exists(),
            msg="Backup file should be created successfully in backup directory.",
        )

    def test_remove_from_file(self):
        """Test that remove records matching the given key from the JSON file and returns True if any records were removed, otherwise False."""
        key_to_remove = "testkey"
        key_value = "testvalue"
        self.assertTrue(
            self.json_services.remove_from_file(key_to_remove, key_value),
            msg="Records matching the given key should be removed from the JSON file and return True if any records were removed, otherwise False.",
        )

    def test_update_data_in_file(self):
        """Test that the method updates records in the JSON file that match the given key with the new data, and returns True if any records were updated, otherwise False."""
        key_to_update = "testkey"
        new_data = {"key": "newvalue"}
        self.assertTrue(
            self.json_services.update_data_in_file(key_to_update, new_data),
            msg="Records in the JSON file that match the given key should be updated with the new data, and return True if any records were updated, otherwise False.",
        )

    def test_get_backup_dir(self):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
