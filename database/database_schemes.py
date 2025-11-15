""" This module defines the database schemas for the library management system. 
    Each schema is represented as a dictionary where keys are field names and values are their expected data types."""

from models.user import valid_roles
from datetime import date, datetime
""" date - if you need only the date, e.g.: date of book return (YYYY-MM-DD)
    datetime - if you need an hour too. """

# In validation implement file format convertion frm text file to type date / datetime
# and checking corectness of file's format

database_schemes = {
    "User" : {
        "id": int,
        "role": list(valid_roles),
        "is_active": bool,
        "last_login": datetime,

        "profile": {
            "user_name": str,
            "first_name": str,
            "last_name": str,
            "email": str,
            "phone_number": int,
            "password_hash": str
        }
    },

    "Book":{
        "id": int,
        "title": str,
        "author": str,
        "isbn": str,
        "publication_year": int,
        "category": str,
        "language": str,
        "book_status": str,
        "borrower_id": str,
        "due_date": date
    }



}


userSchema = {"id": int, "name": str, "email": "str", "role": str}
bookSchema = {"id": int, "title": str, "author": str, "year": int, "isbn": str, "available": bool}
loanSchema = {"id": int, "user_id": int, "book_id": int, "loan_date": str, "return_date": str, "returned": bool}
reservationSchema = {"id": int, "user_id": int, "book_id": int, "reservation_date": str, "fulfilled": bool}
backupSchema = {"file_name": str, "backup_date": str, "size": int}
backupFileSchema = {"file_name": str, "backup_date": str, "size": int}

