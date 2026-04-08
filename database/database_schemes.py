"""This module defines the database schemas for the library management system.
Each schema is represented as a dictionary where keys are field names and values are their expected data types.

Each schema is just a dict of key → Python type


IMPORTANT TO DO:
Schemas here require rebuilding to Json schema style to present required fields. Once schemas are rebuilt, validate_against_schema method from json_files_major_services.py also requires rebuilding to match that approach.

"""

from datetime import date, datetime

from models.user import valid_roles

""" date - if you need only the date, e.g.: date of book return (YYYY-MM-DD)
    datetime - if you need an hour too. """

# In validation implement file format convertion frm text file to type date / datetime
# and checking corectness of file's format


user_schema = {
    "user_id": int,
    "role": str(valid_roles),
    "is_active": bool,
    "last_login": datetime,
    "user_profile": {
        "user_name": str,
        "email": str,
        "phone_number": int,
        "password_hash": str,
    },
}


book_schema = {
    "type": "object",
    "properties": {
        "book_id": {"type": "integer"},
        "title": {"type": "string"},
        "publication_year": {"type": "integer"},
        "author": {"type": "string"},
        "isbn": {"type": "string"},
        "category": {"type": "string"},
        "language": {"type": "string"},
        "book_status": {"type": "string"},
        "borrower_id": {"type": "integer"},
        "due_date": {"type": "string", "format": "date"},
    },
    "required": ["book_id", "title", "publication_year"],
}


loan_schema = {
    "loan_id": int,
    "user_id": int,
    "book_id": int,
    "loan_date": date,
    "return_date": date,
}

reservation_schema = {
    "reservation_id": int,
    "user_id": int,
    "book_id": int,
    "reservation_date": date,
}

backup_schema = {"file_name": str, "backup_date": date}
