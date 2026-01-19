"""
__________________________________________________________
database.loan_json_file_service
==========================================================
Service class for managing book loan data in a JSON file.
__________________________________________________________

TO DO HERE: 
- Delete permission checks in all methods. <-- Checking permissions will go to functionality layer. 
- verify imports
- update docstrings

METHODS:
1. get_loan_data() --> implemented
2. add_loan() --> implemented
3. get_all_loans_list() --> implemented
4. update_file data() --> reviewed
5. delete_data_from_file() --> reviewed

--> General review of methods.
"""



import exceptions as exc

from utils.config import LOANS_LIST_FILE_PATH
from database.json_files_major_services import JsonFilesService
from services.authorisation_service import UserAuthorisation

class LoanJsonFileService():
    """ Service class for managing book loan data in a JSON file. This class provides methods to add, retrieve, update, and delete book loan records,
        while ensuring data validation. It can be used to manage the library's book loan records.
    """
    def __init__(self, json_service: JsonFilesService, authorisation: UserAuthorisation, file_path=LOANS_LIST_FILE_PATH):
        self.json_service = json_service
        self.authorisation = authorisation
        self.file_path = file_path

    def get_loan_data(self, loan_id):
        """ This method retrieves loan data from record in database file by loan ID. It returns loan data as dictionary. It can be used to display single loan details in GUI.

        Args:
            loan_id (int): Unique number of loan

        Returns:
            dict: Loan data as a dictionary.
        """
        current_data = self.json_service.load_json_file()
        loan_found = False
        loan_data = None

        for loan in current_data:
            if loan["loan_id"] == loan_id:
                loan_data = loan
                loan_found = True

        if not loan_found:
            raise exc.LoanNotFoundError(f"Loan with {loan_id} does not exists in database.")
        
        return loan_data
        

    def add_loan_data(self, loan_data):
        """ This method adds new loan data record to database file. It validates loan_data against schema and checks uniqueness of loan ID. It can be used to create new loan record.
        This method works with all kinds of loan actions - new loan, return of book, extend loan period.

        Args:
            loan_data (dict): Loan data to be added to database.

        Returns:
            str: Confirmation message that new loan data record was added to the database.
        """
        current_data = self.json_service.load_json_file()
        validated_loan_data = self.json_service.validate_against_schema(loan_data)
        loan_id = loan_data["loan_id"]

        if not loan_data:
            raise exc.DataError("Book data to save is missing or it's incorrect.")
        
        if not isinstance(loan_data, dict):
            raise exc.DataTypeError("Book data type is incorrect. Book data must be a dictionary")
        
        for loan in current_data:
            if loan["loan_id"] == loan_id:
                raise exc.LoanError(f"Loan with ID: {loan['loan_id']} exists in the database. ID number must be unique value.")
            
        if not validated_loan_data:
            raise exc.LoanValidationError("Validation failed. Book data doesn't match database file schema.")
        else:
            current_data.append(loan_data)

        self.json_service.write_json_data(current_data)

        return "New loan record added to the database without errors."
    

    def get_all_loans_list(self, loan_id):
        """ This method returns list of all loans in database. It can be used to display all loans in GUI and makes possible to manage on the loans (searching, deleting, updating etc.)

        Args:
            loan_id (int): Unique numerber of loan 

        Returns:
            list: This method returns a list of all loans in database file. 
        """
        current_data = self.json_service.load_json_file()
        self.get_loan_data(loan_id)
        all_loans_list = []
        loan_found = False

        for loan in current_data:
            if loan["loan_id"] == loan_id:
                try:
                    all_loans_list.append(loan)
                    loan_found = True
                except KeyError:
                    raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found.")
            if not loan_found:
                raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found.")
        return all_loans_list
            
        
    def update_file_data(self, loan_id, field, new_value):
        """ This method updates existing loan record in the JSON file with new data. It can be used to update loan details such as return date, loan status, etc.
        Args:
            loan_id (int): The ID of the loan to update.
            field (str): The field to update.
            new_value: The new value to set for the specified field.
        Returns:
            str: Confirmation message that loan data was updated successfully.
        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_loan_data(loan_id)
        loan_id_found = False

        if not new_value:
            raise exc.LoanValidationError("New value to update loand data is missing or is not correct.")
        
        for loan in current_data:
            if loan["id"] == loan_id:
                try:
                    loan[field] = new_value
                    loan_id_found = True
                except KeyError:
                    raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found in database.")
                
            if not loan_id_found:
                raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found in database.")

        self.json_service.validate_against_schema()    
        self.json_service.write_json_data(current_data)
        return f"For loan with ID: {loan_id}, data updated successfully."


    def delete_data_from_file(self, loan_id):
        """ This method deletes loan record from the JSON file by loan ID. It can be used to remove loan records that are no longer needed.
        Args:
            loan_id (int): The ID of the loan to delete.
        Returns:
            str: Confirmation message that loan record was deleted successfully.
        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_loan_data(loan_id)
        loan_id_found = False

        for loan in current_data:
            if loan["id"] == loan_id:
                current_data.remove(loan)
                loan_id_found = True

        if not loan_id_found:
            raise exc.LoanNotFoundError("Loan ID to delete record is incorrect or missing in the loans database file.")

        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"Loan record with ID {loan_id} has been deleted from database."