"""
__________________________________________________________
database.loan_json_file_service
==========================================================
Service class for managing book loan data in a JSON file.
__________________________________________________________

Loan JSON storage service.

This module provides a high‑level interface for managing book loan records stored in
a JSON file. It supports adding new loans, retrieving individual records, listing
loans, updating loan details, and deleting loan entries. All I/O operations and schema
validation are delegated to JsonFilesService, ensuring consistent data handling across
the application.

"""

import database.database_schemes as schema
import exceptions as exc
from database.json_files_major_services import JsonFilesService
from utils.config import LOANS_LIST_FILE_PATH


class LoanJsonFileService:
    """High‑level operations for loan records stored in a JSON file.

    Provides helper methods to load, modify, validate, and delete loan entries.
    Works together with JsonFilesService to maintain correct structure and data integrity.
    """

    def __init__(self, json_service: JsonFilesService, file_path=LOANS_LIST_FILE_PATH):
        self.json_service = json_service
        self.file_path = file_path

    def get_loan_data(self, loan_id):
        """Retrieve a single loan record by loan ID.

        Args:
            loan_id (int): Identifier of the loan to fetch.

        Returns:
            dict: Matching loan record.

        Raises:
            exc.LoanNotFoundError: If the loan does not exist.
        """
        current_data = self.json_service.load_json_file()
        loan_found = False
        loan_data = None

        if loan_id == None:
            raise exc.ValidationError(
                "Loan ID is missing or it's an empty value.")

        for loan in current_data:
            if loan["loan_id"] == loan_id:
                loan_data = loan
                loan_found = True
                break

        if not loan_found:
            raise exc.LoanNotFoundError(
                f"Loan with {loan_id} does not exists in database."
            )

        return loan_data

    def add_loan_data(self, loan_data):
        """Add a new loan record.

        Validates the incoming data against the schema, checks the loan ID for uniqueness,
        and saves the updated list back to the JSON file. Supports new loans, returns,
        and loan extensions.

        Args:
            loan_data (dict): Loan details to store.

        Returns:
            str: Confirmation message.

        Raises:
            exc.DataError: If input data is missing.
            exc.DataTypeError: If the payload is not a dict.
            exc.LoanError: If the loan ID already exists.
            exc.LoanValidationError: If schema validation fails.
        """
        current_data = self.json_service.load_json_file()

        if not loan_data:
            raise exc.DataError(
                "Book data to save is missing or it's incorrect.")

        if not isinstance(loan_data, dict):
            raise exc.DataTypeError(
                "Book data type is incorrect. Book data must be a dictionary"
            )
        loan_id = loan_data["loan_id"]
        for loan in current_data:
            if loan["loan_id"] == loan_id:
                raise exc.LoanError(
                    f"Loan with ID: {loan['loan_id']} exists in the database. ID number must be unique value."
                )
        validated_loan_data = self.json_service.validate_against_schema(
            loan_data, schema.loan_schema)

        if not validated_loan_data:
            raise exc.LoanValidationError(
                "Validation failed. Book data doesn't match database file schema."
            )
        else:
            current_data.append(loan_data)

        self.json_service.write_json_data(current_data)

        return "New loan record added to the database without errors."

    def get_all_loans_list(self, loan_id):
        """This method SHOULD return list of all loans in database.

        Return all loans matching a given ID.

        Note: The method keeps the original behavior, even though the name suggests
        listing all loans. It filters the records using the given ID.

        Args:
            loan_id (int): Loan identifier.

        Returns:
            list: List of matching loan records.

        Raises:
            exc.LoanNotFoundError: If no matching records are found.

        """
        current_data = self.json_service.load_json_file()
        all_loans_list = []
        loan_found = False

        for loan in current_data:
            if loan["loan_id"]:
                all_loans_list.append(loan)
                loan_found = True
            else:
                raise exc.LoanNotFoundError(
                    f"Loan with ID: {loan_id} not found.")

        if not loan_found:
            raise exc.LoanNotFoundError(f"Loan with ID: {loan_id} not found.")

        return all_loans_list

    def update_file_data(self, loan_id, field, new_value):
        """Update an existing loan record.

        Loads the JSON data, ensures the loan exists, updates the selected field,
        validates the modified structure, and saves the updated file.

        Args:
            loan_id (int): Identifier of the loan to update.
            field (str): Field name to modify.
            new_value: New value to assign.

        Returns:
            str: Confirmation message.

        Raises:
            exc.LoanValidationError: If new_value is missing.
            exc.LoanNotFoundError: If the loan or field cannot be updated.
        """
        self.json_service.file_exists_checking()
        current_data = self.json_service.load_json_file()
        self.get_loan_data(loan_id)
        loan_id_found = False

        if not new_value:
            raise exc.LoanValidationError(
                "New value to update loand data is missing or is not correct."
            )

        for loan in current_data:
            if loan["id"] == loan_id:
                try:
                    loan[field] = new_value
                    loan_id_found = True
                except KeyError:
                    raise exc.LoanNotFoundError(
                        f"Loan with ID: {loan_id} not found in database."
                    )

            if not loan_id_found:
                raise exc.LoanNotFoundError(
                    f"Loan with ID: {loan_id} not found in database."
                )

        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"For loan with ID: {loan_id}, data updated successfully."

    def delete_data_from_file(self, loan_id):
        """Delete a loan entry from the JSON file.

        Loads the file, verifies the loan exists, removes the matching record,
        validates updated data, and saves the final version.

        Args:
            loan_id (int): Identifier of the loan to remove.

        Returns:
            str: Confirmation message.

        Raises:
            exc.LoanNotFoundError: If the loan cannot be deleted.
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
            raise exc.LoanNotFoundError(
                "Loan ID to delete record is incorrect or missing in the loans database file."
            )

        self.json_service.validate_against_schema()
        self.json_service.write_json_data(current_data)
        return f"Loan record with ID {loan_id} has been deleted from database."
