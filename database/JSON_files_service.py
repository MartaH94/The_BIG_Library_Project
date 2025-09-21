# access to database, saving and reading library data from JSON file

import json
import utils.config as config
import exceptions as exc
from pathlib import Path
from datetime import datetime

class JsonFilesService():
    def __init__(self, file_path: Path):
        self.file_path = file_path
        
    def read_json_file(self):
        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
        except FileNotFoundError:
            raise exc.FileNotFound(f"File doesn't exists in catalogue: {self.file_path.name}")

    def write_json_data(self, data):
        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def append_data_to_file(self, data_to_append): 
        self.file_exists_checkout()

        current_data = self.read_json_file() 
        current_data.append(data_to_append)
        self.write_json_data(current_data)

        return f"Data had been saved to file: {self.file_path.name}"

    def file_exists_checkout(self):
        if not self.file_path.exists():
            self.write_json_data([])
            return "Created new file with empty list."
        else:
            return "The file exists. You can continue."
        
    def create_backup_file(self):
        if not self.file_path.exists():
            raise exc.FileNotFound("File not found in the folder.")
        
        name = self.file_path.stem
        subfolder_backup = config.BACKUP_FILES_DIRECTORY/ name

        if not subfolder_backup.exists():
            subfolder_backup.mkdir(parents=True, exist_ok=True)

        alias = config.PROJECT_ALIAS
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        backup_file_name = f"{alias}_{name}_{timestamp}.json"
        backup_file_path = subfolder_backup/backup_file_name

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise exc.FileError(f"Cannot read JSON file: {e}")
            
        with backup_file_path.open("w", encoding="utf-8") as f_backup:
            json.dump(data, f_backup, ensure_ascii=False, indent=4)

        return backup_file_path


    def validate_file_data(self):
        pass



        

# read user from users list - plik program_users.json
# read library from file - plik the_awesome_library.json
# read list of loans - plik list_of_loans.json
# read user's list of loan - plik single_user_history.json

# saving data in database