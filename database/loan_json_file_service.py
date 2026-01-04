"""
__________________________________________________________
database.loan_json_file_service
==========================================================
Service class for managing book loan data in a JSON file.
__________________________________________________________

TO DO HERE: 
- verify imports
- update docstrings
- implement crucial methods

methods to implement: get full list of loans, verificate correct loan data, add loan data to database, update data in loan, what else I can do with that data? 



"""







import json
import utils.config as config
import exceptions as exc

from utils.config import PROGRAM_USERS_FILE_PATH
from database.json_files_major_services import JsonFilesService
from services.authorisation_service import UserAuthorisation

class LoanJsonFileService():
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=PROGRAM_USERS_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def update_file_data(self, loan_id, field, new_value):
        self.authorisation.check_permission("edit_data")
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()

        if not new_value:
            return "Information to user, that new value can not be empty field"
        
        loan_id_found = False
        for loan in current_data:
            if loan["id"] == loan_id:
                try:
                    loan[field] = new_value
                    loan_id_found = True
                except KeyError:
                    raise exc.InvalidFieldError(f"Field {field} does not exists in loan database file.")
                
            if not loan_id_found:
                raise exc.LoanNotFoundError(f"Loan id {loan_id} is missing in the loans file. ")
            
        self.json_service.write_json_data(current_data)
        return "Placeholder, confirmation for user."

    def delete_data_from_file(self, loan_id):
        self.authorisation.check_permission("delete_data")
        self.json_service.file_exists_checking
        current_data = self.json_service.load_json_file()
        
        if not loan_id:
            raise exc.LoanValidationError("Loan data are empty field or have invalid value.")
        
        loan_id_found = False
        for loan in current_data:
            if loan["id"] == loan_id:
                current_data.remove(loan)
                loan_id_found = True

        if not loan_id_found:
            raise exc.LoanNotFoundError("Loan ID does not exists in the loans file.")

        self.json_service.write_json_data(current_data)
        return "Placeholder to confiramtion to user that data has benn deleted."