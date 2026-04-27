"""
________________________________________________________
tests.test_user_json_file_service.py
========================================================
Test for the file user_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 20

current status: not started
Total number of done test cases:

TO DO:
Verify existing test cases
Add new test cases if needed

"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.loan_json_file_service import LoanJsonFileService
from database.user_json_file_service import UsersJsonFileService


class TestUserServiceGetUserData(unittest.TestCase):
    """Method under test: get_user_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_user_data_when_id_exists(self):
        pass

    def test_raises_validation_error_when_user_id_is_none(self):
        pass

    def test_raises_user_not_found_error_when_id_does_not_exist(self):
        pass


class TestUserServiceAddUserData(unittest.TestCase):
    """Method under test: add_user_data
    Number of TestCases: 5
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_appends_validated_user_data_and_writes_to_file(self):
        pass

    def test_raises_validation_error_when_user_data_is_missing(self):
        pass

    def test_raises_data_type_error_when_user_data_is_not_dict(self):
        pass

    def test_raises_user_error_when_user_id_already_exists(self):
        pass

    def test_raises_user_validation_error_when_schema_validation_fails(self):
        pass


class TestUserServiceGetAllUsersList(unittest.TestCase):
    """Method under test: get_all_users_list
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_users_when_user_name_present(self):
        pass

    def test_raises_user_not_found_error_when_user_name_missing_or_empty(self):
        pass

    def test_raises_user_not_found_error_when_does_not_exists(self):
        pass


class TestUserServiceUpdateUserData(unittest.TestCase):
    """Method under test: update_user_data
    Number of TestCases: 6
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_updates_existing_user_field_and_writes_data(self):
        pass

    def test_raises_validation_error_when_user_id_is_none(self):
        pass

    def test_raises_validation_error_when_field_is_none(self):
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        pass

    def test_raises_validation_error_when_field_missing_in_user_entry(self):
        pass

    def test_raises_user_not_found_error_when_user_id_not_found(self):
        pass


class TestUserServiceDeleteUserById(unittest.TestCase):
    """Method under test: delete_user_by_id
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_removes_user_when_id_exists_and_writes_data(self):
        pass

    def test_raises_validation_error_when_user_id_is_none(self):
        pass

    def test_raises_user_error_when_user_id_not_found_for_deletion(self):
        pass
