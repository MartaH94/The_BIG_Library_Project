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
        pass


class TestBookJsonFileServiceAddBookData(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestBookJsonFileServiceGetAllBooksList(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestBookJsonFileServiceUpdateBookData(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()


class TestBookJsonFileServiceDeleteBookById(unittest.TestCase):
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()
