"""
________________________________________________________
tests.test_book_json_file_service.py
========================================================
Test for the file book_json_file_service.py
________________________________________________________

Test classes:
Test cases total:

current status: not started
Total number of done test cases:

"""

import json
import tempfile
import unittest

import exceptions as exc
from database.book_json_file_service import BookJsonFileService


class TestBookJsonFileServiceGetBookData(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        pass

    def test_returns_book_when_book_id_exists(self):
        pass

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        pass


class TestBookJsonFileServiceAddBookData(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_data_is_missing(self):
        pass

    def test_raises_data_type_error_when_book_data_is_not_dict(self):
        pass

    def test_raises_book_error_when_book_id_already_exists(self):
        pass

    def tets_raises_book_validation_error_when_schema_validation_fails(self):
        pass

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        pass


class TestBookJsonFileServiceGetAllBooksList(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_books_when_database_is_not_empty(self):
        pass

    def test_raises_book_not_found_error_when_database_is_empty(self):
        pass


class TestBookJsonFileServiceUpdateBookData(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        pass

    def test_raises_validation_error_when_field_is_none(self):
        pass

    def test_raises_validation_error_when_new_value_is_none(self):
        pass

    def test_raises_validation_error_when_field_not_in_book(self):
        pass

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        pass

    def test_updates_book_and_writes_json_when_data_is_valid(self):
        pass


class TestBookJsonFileServiceDeleteBookById(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        pass

    def test_raises_book_error_when_book_id_not_found(self):
        pass

    def test_removes_book_and_writes_json_when_book_id_exists(self):
        pass
