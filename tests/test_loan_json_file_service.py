"""
________________________________________________________
tests.test_loan_json_file_service.py
========================================================
Test for the file loan_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 20

current status: not started
Total number of done test cases:

IMPORTANT:
loan_schema (database_schemes.py) requires rebuilding to Json schema style to prepare required fields. Otherwise all fields must be filles during adding book data.

verify test cases after implementation of that changes.
"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.json_files_major_services import JsonFilesService
from database.loan_json_file_service import LoanJsonFileService


class TestLoanJsonFileServiceGetLoanData(unittest.TestCase):
    """Method under test: get_loan_data
    Number of TestCases: 3
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_matching_record_for_existing_id(self):
        pass

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        pass


class TestLoanJsonFileServiceAddLoanData(unittest.TestCase):
    """Method under test: add_loan_data
    Number of TestCases: 5
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_appends_valid_loan_and_writes_file(self):
        pass

    def test_raises_validation_error_when_loan_data_is_missing(self):
        pass

    def test_raises_data_type_error_when_loan_data_is_not_dict(self):
        pass

    def test_raises_loan_error_when_loan_id_already_exists(self):
        pass

    def test_raises_loan_validation_error_when_schema_validation_fails(self):
        pass


class TestLoanJsonFileServiceGetAllLoansList(unittest.TestCase):
    """Method under test: get_all_loans_list
    Number of TestCases: 2
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_list_when_file_content_is_list(self):
        pass

    def test_raises_data_type_error_when_file_content_is_not_list(self):
        pass


class TestLoanJsonFileServiceUpdateLoanData(unittest.TestCase):
    """Method under test: update_loan_data
    Number of TestCases: 6
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_updates_field_and_writes_file_when_loan_exists(self):
        pass

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_raises_validation_error_when_field_is_none(self):
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        pass

    def test_raises_validation_error_when_field_not_in_loan(self):
        pass

    def test_raises_loan_not_found_error_when_load_id_not_found(self):
        pass


class TestLoanJsonFileServiceDeleteLoanDataFromFile(unittest.TestCase):
    """Method under test: delete_loan_data
    Number of TestCases: 4
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_removes_loan_and_writes_file_when_id_exists(self):
        pass

    def test_raises_validation_error_when_loan_id_is_none(self):
        pass

    def test_raises_data_type_error_when_loan_id_is_not_int(self):
        pass

    def test_raises_loan_not_found_error_when_loan_id_not_found(self):
        pass
