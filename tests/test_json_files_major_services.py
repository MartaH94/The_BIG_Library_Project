"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

TO DO HERE:
- Create unit tests for all methods in json_files_major_services module. method by method.

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


class TestMethodFileExistsChecking(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
