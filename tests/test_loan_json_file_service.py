"""
________________________________________________________
tests.test_loan_json_file_service.py
========================================================
Test for the file loan_json_file_service.py
________________________________________________________

Test classes:
Test cases total:

current status: not started
Total number of done test cases:

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
    Number of TestCases:
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceAddLoanData(unittest.TestCase):
    """Method under test: add_loan_data
    Number of TestCases:
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceGetAllLoansList(unittest.TestCase):
    """Method under test: get_all_loans_list
    Number of TestCases:
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceUpdateLoanData(unittest.TestCase):
    """Method under test: update_loan_data
    Number of TestCases:
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestLoanJsonFileServiceDeleteLoanDataFromFile(unittest.TestCase):
    """Method under test: delete_loan_data
    Number of TestCases:
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()
