"""
________________________________________________________
tests.test_json_files_major_service.py
========================================================
Test for the file json_files_major_services.py
________________________________________________________

TO DO HERE:
- Create unit tests for all methods in json_files_major_services module. method by method.

Test cases should cover behaviors for all methods, including edge cases and error handling.




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


# -------------------------
# File I/O helpers
# -------------------------
class TestMethodFileExistsChecking(unittest.TestCase):
    pass


class TestMethodLoadJsonFile(unittest.TestCase):
    pass


class TestMethodWriteJsonData(unittest.TestCase):
    pass

# -------------------------
# CRUD operations
# -------------------------


class TestMethodAppendDataToFile(unittest.TestCase):
    pass

# -------------------------
# Core validation
# -------------------------


class TestMethodValidateAgainsSchema(unittest.TestCase):
    pass


class TestMethodValidateFileData(unittest.TestCase):
    pass

# -------------------------
# Backup helpers
# -------------------------


class TestMethodGetOrCreateBackupDir(unittest.TestCase):
    pass


class TestMethodBuildBackupFileName(unittest.TestCase):
    pass


class TestMethodCreateBackupFile(unittest.TestCase):
    pass

# -------------------------
# Remove/Update operations
# -------------------------


class TestMethodRemoveFromFile(unittest.TestCase):
    pass


class TestMethodUpdateDataInFile(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
