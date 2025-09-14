# basic settings of the project like file paths, database parameters, etc.

import os
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "program_data"
DATA_DIR.mkdir(exist_ok=True)   # If the catalog (program_data) exists, no action needed.

LOANS_LIST_FILE_PATH = DATA_DIR / "list_of_loans.json"
PROGRAM_USERS_FILE_PATH = DATA_DIR / "program_users.json"
SINGLE_USER_LOANS_FILE_PATH = DATA_DIR / "single_user_history.json"
THE_LIBRARY_FILE_PATH = DATA_DIR / "the_awesome_library.json"

