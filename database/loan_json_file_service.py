"""
__________________________________________________________
database.loan_json_file_service
==========================================================
Service class for managing book loan data in a JSON file.
__________________________________________________________

TO DO HERE: 
- verify imports
- update docstrings

METHODS:
1. get_loan_data() --> implement
2. add_loan() --> implement
3. get_all_loans_list() --> implement
4. update_file data() --> make review
5. delete_data_from_file() --> make review


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

    def get_loan_data(self, loan_id):
        current_data = self.json_service.load_json_file()
        loan_found = False
        loan_data = None

        for loan in current_data:
            if loan["loan_id"] == loan_id:
                loan_data = loan
                loan_found = True

        if not loan_found:
            raise exc.BookNotFoundError(f"Loan with {loan_id} does not exists in database.")
        
        return loan_data
        

    def add_loan_data(self, loan_data):
        current_data = self.json_service.load_json_file()
        validated_loan_data = self.json_service.validate_against_schema(loan_data)
        loan_id = loan_data["loan_id"]

        if not loan_data:
            raise exc.DataError("Book data to save is missing or it's incorrect.")
        
        if not isinstance(loan_data, dict):
            raise exc.DataTypeError("Book data type is incorrect. Book data must be a dict type.")
        
        for loan in current_data:
            if loan["loan_id"] == loan_id:
                raise exc.BookError(f"Book with ID: {loan["loan_id"]} exists in the database. ID number must be unique value.")
            
        if not validated_loan_data:
            raise exc.BookValidationError("Validation failed. Book data doesn't match database file schema.")
        else:
            current_data.append(loan_data)

        self.json_service.write_json_data(current_data)

        return "New book record added to the database without errors."
    

    def get_all_loans_list(self):
        pass

    def update_file_data(self, loan_id, field, new_value):
        """ !! This method needs review.
        """
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
        """ !! This method requires review! 
        """
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