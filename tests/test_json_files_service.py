# unit tests for json_files_service.py

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
        """Test that the JSON file existence check works and creates a new file if needed."""
        file_to_check = self.json_services.file_path
        self.json_services.file_exists_checking()
        with open(file_to_check, encoding="utf-8") as f:
            file_content = json.load(f)

        self.assertEqual(file_content, [], msg="Checking if the json file exist. If not, should create a new file with empty list and return status ok.")


    def test_checking_file_open(self):
        """Test that the file open operation can be performed without errors."""
        file_to_open = self.json_services.file_path
         
        self.json_services.read_json_file()
        with open(file_to_open, encoding="utf-8") as f:
            f.read()

        

    def test_validate_file_data_(self):
        """Test that the data in the file is not corrupt."""
        file_to_validate = self.json_services.file_path
        self.json_services.validate_file_data()
        
        
        
        
        
        
        with open(file_to_validate, encoding="utf-8") as f:
            f.read()



    def test_check_file_returns_correct_data(self):
        """Test that the file after opening operation is displaying correct data."""
        pass







if __name__ == '__main__':
    unittest.main(verbosity=2)

