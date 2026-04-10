"""This module defines the database schemas for the library management system.
Each schema is represented as a dictionary where keys are field names and values are their expected data types.


"""

from models.user import valid_roles

user_schema = {
    "fields": {
        "user_id": int,
        "role": (
            "one_of",
            valid_roles,
        ),  # role must be one of the valid roles defined in the system
        "is_active": bool,
        "last_login": "datetime",  # string representation of datetime
        "user_profile": {
            "fields": {
                "user_name": str,
                "email": str,
                "phone_number": int,
                "password_hash": str,
            },
            "required": ["user_name", "email"],
        },
    },
    "required": ["user_id", "role", "user_profile"],
}


book_schema = {
    "fields": {
        "book_id": int,
        "title": str,
        "publication_year": int,
        "author": str,
        "isbn": str,
        "category": str,
        "language": str,
        "book_status": str,
        "borrower_id": (
            int,
            type(None),
        ),  # borrower_id can be an integer (user_id) or None if the book is not currently loaned out
        "due_date": "date",  # stored as string
    },
    "required": ["book_id", "title", "publication_year"],
}


loan_schema = {
    "fields": {
        "loan_id": int,
        "user_id": int,
        "book_id": int,
        "loan_date": "date",
        "return_date": ("date", type(None)),
    },
    "required": ["loan_id", "user_id", "book_id", "loan_date"],
}

reservation_schema = {
    "reservation_id": int,
    "user_id": int,
    "book_id": int,
    "reservation_date": "date",
}

backup_schema = {"file_name": str, "backup_date": "datetime"}
