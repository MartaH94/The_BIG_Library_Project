# unit tests for json_files_service.py

import unittest
import tempfile
import shutil
import json

from models import user
from services.authorisation_service import UserAuthorisation
import database.JSON_files_service as json_services
from pathlib import Path
from utils import config
import exceptions as exc

class TestJsonServices(unittest.TestCase):
    def setUp(self):
        self.json_services = json_services.JsonFilesService()

        self.admin_user = user.User(user_id="Marta.Boss", email="marta@mail.com", role="admin")
        self.admin_authorisation = UserAuthorisation()
        self.admin_authorisation.login(self.admin_user)

        self.reader_user = user.User(user_id="Andrzej.czytelnik", email="read@andrew.com", role="reader")
        self.reader_authorisation = UserAuthorisation()
        self.reader_authorisation.login(self.reader_user)

