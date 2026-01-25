"""
________________________________________________________
tests.test_json_files_service
========================================================
Test Class for json_files_major_services module.
________________________________________________________

TO DO HERE:
- Create unit tests for all methods in json_files_major_services module.

Test cases should cover behaviors for all methods, including edge cases and error handling.

List of tests to implement:
- test_checking_file_exists
- test_loading_json_file
- test_validate_file_data
- test_create_backup_file
- test_remove_from_file
- test_update_data_in_file
- test_write_json_data
- test_get_or_create_backup_dir
- test_build_backup_file_name
- test_check_file_returns_correct_data
- test_exceptions_handling_in_methods


"""


import unittest
import tempfile
import json

from models.user import User
from services.authorisation_service import UserAuthorisation
import database.json_files_major_services as json_files_major_services


from pathlib import Path
import utils.config as config
import exceptions as exc
from unittest import TestCase

class TestJsonServices(TestCase):
    def setUp(self):
        self.admin_user = User(user_id="Marta.Boss", email="marta@mail.com", role="admin")
        self.admin_authorisation = UserAuthorisation()
        self.admin_authorisation.login(self.admin_user)

        self.reader_user = User(user_id="Andrzej.czytelnik", email="read@andrew.com", role="reader")
        self.reader_authorisation = UserAuthorisation()
        self.reader_authorisation.login(self.reader_user)

        self.test_directory = tempfile.TemporaryDirectory()
        self.test_file = Path(self.test_directory.name)/"testing_file.json"
        self.test_file.write_text("[]", encoding="utf-8")
        self.json_services = json_files_major_services.JsonFilesService(file_path=self.test_file)


    def tearDown(self):
        self.test_directory.cleanup()


    def test_checking_file_exists(self):    # test ok
        """ Test checking if the json file exist. If not, should create a new file with empty list and return status ok."""
        file_to_check = self.json_services.file_path
        self.json_services.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, [], msg="Checking if the json file exist. If not, should create a new file with empty list and return status ok.")


    def test_load_json_file(self):
        """ Test that the file load operation can be performed without errors,verifies the returned data type is a list, 
            and ensures the file remains readable after loading.
        """
        result = self.json_services.load_json_file()
        self.assertIsInstance(result, list, msg="The loaded JSON data from load_json_file() should be a list.")
        

    def test_write_json_data(self):
        #self.data_to_write = self.json_services.???
        self.data_to_write = [{"key": "value"}, {"number": 123}]
        self.saved_data = self.json_services.write_json_data(self.data_to_write)
        self.assertTrue(self.saved_data, msg="Data should be written to the JSON file successfully.")
        

    def test_append_data_to_file(self):
        self.data_to_append = {"key" : "value"}
        self.adding_data = self.json_services.append_data_to_file(self.data_to_append)
        self.assertTrue(self.adding_data, msg="New record data should be saved in JSON file successfully.")
        pass


    def test_validate_data_against_schema(self):
        pass


    def test_validate_file_data(self):
        """ Test that the data in the file is list"""
        data_to_validate = self.json_services.load_json_file()
        self.json_services.validate_file_data(data_to_validate, self.json_services.schema)
        self.assertIsInstance(data_to_validate, dict, msg="Validation data against schema should confirm data is a dict.")
                
        
    def test_get_or_create_backup_dir(self):
        pass


    def test_build_backup_filename(self):
        pass


    def test_create_backup_file(self):
        """ Test that the backup file is created.
        """
        pass


    def test_remove_from_file(self):
        pass


    def test_update_data_in_file(self):
        pass


    


    


    def test_get_backup_dir(self):
        pass


    




if __name__ == '__main__':
    unittest.main(verbosity=2)

