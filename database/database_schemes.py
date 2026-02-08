"""This module defines the database schemas for the library management system.
Each schema is represented as a dictionary where keys are field names and values are their expected data types.

Each schema is just a dict of key → Python type

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
    }
}

book_schema = {
    "book_id": int,
    "title": str,
    "author": str,
    "isbn": str,
    "publication_year": int,
    "category": str,
    "language": str,
    "book_status": str,
    "borrower_id": int,
    "due_date": date,
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
