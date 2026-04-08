"""
________________________________________________________
tests.test_book_json_file_service.py
========================================================
Test for the file book_json_file_service.py
________________________________________________________

Test classes: 5
Test cases total: 18

current status: in progress
Total number of done test cases: 3

"""

import json
import tempfile
import unittest
from pathlib import Path

import exceptions as exc
from database.book_json_file_service import BookJsonFileService
from database.json_files_major_services import JsonFilesService


class TestBookJsonFileServiceGetBookData(unittest.TestCase):  # 3/3
    """Method under test: get_book_data
    Number of TestCases: 3
    Done TestCases: 3
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"

        self.valid_book_list = [
            {"book_id": 1001, "author": "Stephen King", "title": "It", "year": 1986},
            {"book_id": 1002, "author": "Frank Herbert", "title": "Dune", "year": 1965},
            {"book_id": 1003, "author": "Jane Austen", "title": "Emma", "year": 1815},
            {
                "book_id": 1004,
                "author": "Peter Benchley",
                "title": "Jaws",
                "year": 1974,
            },
        ]

        with self.test_json_file_path.open("w", encoding="utf-8") as f:
            json.dump(self.valid_book_list, f)

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_id_is_none(self):
        """expected behavior: raises ValidationError when book_id is None"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.get_book_data(None)

        self.assertIn("Book ID is missing", str(cm.exception))

    def test_returns_book_when_book_id_exists(self):
        """expected behavior: returns book data when book_id exists in the database"""
        expected_book_data = self.valid_book_list[0]
        test_result = self.book_service.get_book_data(1001)
        self.assertEqual(test_result, expected_book_data)

    def test_raises_book_not_found_error_when_book_id_not_found(self):
        """expected behavior: raises BookNotFoundError when book_id is not found in the database"""
        with self.assertRaises(exc.BookNotFoundError) as cm:
            self.book_service.get_book_data(1006)

        self.assertIn("not exists in database", str(cm.exception))


class TestBookJsonFileServiceAddBookData(unittest.TestCase):  # 0/5
    """Method under test: add_book_data
    Number of TestCases: 5
    Done TestCases:
    """

    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()
        self.temporary_dir_path = Path(self.temporary_dir.name)
        self.test_json_file_path = self.temporary_dir_path / "test_file.json"
        self.test_json_file_path.write_text("[]", encoding="utf-8")

        self.major_json_service = JsonFilesService(file_path=self.test_json_file_path)

        self.book_service = BookJsonFileService(
            self.major_json_service, file_path=self.test_json_file_path
        )

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_raises_validation_error_when_book_data_is_missing(self):
        """expected behavior: raises ValidationError when book data is missing or it's an empty value"""
        with self.assertRaises(exc.ValidationError) as cm:
            self.book_service.add_book_data(None)

        self.assertIn("Book data to save is missing.", str(cm.exception))

    def test_raises_data_type_error_when_book_data_is_not_dict(self):
        """expected behavior: raises DataTypeError when book data is not a dict type"""
        data_to_add = [1005, "William Shakespeare", "Macbeth", 1606]

        with self.assertRaises(exc.DataTypeError) as cm:
            self.book_service.add_book_data(data_to_add)

        self.assertIn("Book data type is incorrect.", str(cm.exception))

    def test_raises_book_error_when_book_id_already_exists(self):
        """expected behavior: raises BookError when book_id already exists in the database"""
        pass

    def tets_raises_book_validation_error_when_schema_validation_fails(self):
        """expected behavior: raises BookValidationError when book data doesn't match database file schema"""
        invalid_book_data = {}
        pass

    def test_writes_json_and_returns_success_message_when_data_is_valid(self):
        """expected behavior: writes new book data to json file and returns success message when book data is valid"""
        pass


class TestBookJsonFileServiceGetAllBooksList(unittest.TestCase):  # 0/2
    def setUp(self):
        self.temporary_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temporary_dir.cleanup()

    def test_returns_all_books_when_database_is_not_empty(self):
        pass

    def test_raises_book_not_found_error_when_database_is_empty(self):
        pass


class TestBookJsonFileServiceUpdateBookData(unittest.TestCase):  # 0/6
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


class TestBookJsonFileServiceDeleteBookById(unittest.TestCase):  # 0/3
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


if __name__ == "__main__":
    unittest.main(verbosity=0)
