# access to database, saving and reading library data from JSON file

import json
import utils.config as config
from pathlib import Path

class JsonFilesService():
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def read_json_file(self):
        with self.file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def write_json_data(self, data):
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def append_data_to_file(self):
        pass

    def update_file_data(self):
        pass

    def delete_data_from_file(self):
        pass

    def file_exists_checkout(self):
        pass


# 1. imports    2. function for all functions   3. Save to file function



# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database