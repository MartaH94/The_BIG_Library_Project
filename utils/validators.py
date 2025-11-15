# functions to validate user inputs, eg. login, credentials, etc. 
# "librarian", "guest", "moderator"

from models.user import User

user_permissions = {
    "reader" : {
        "borrow_book" : True,
        "return_book" : True,
        "book_the_book" : True,
        "approve_reservations": True,
        "view_books" : True,
        "view_borrow_history": True,
        "add_book" : True,
        "edit_book" : False,
        "delete_book" : False,
        "search_book" : True,
        "manage_users" : False,
        "update_account": False,
        "delete_data" : False,
        "edit_data" : False
    },
    "admin": {
        "borrow_book" : False,
        "return_book" : False,
        "book_the_book" : False,
        "approve_reservations": True,
        "view_books" : True,
        "view_borrow_history": True,
        "add_book" : True,
        "edit_book" : True,
        "delete_book" : True,
        "search_book" : True,
        "manage_users" : True,
        "update_account": True,
        "delete_data" : True,
        "Edit_data" : True
    },
    "librarian": {
        "borrow_book": False
    },
    "guest": {
        "borrow_book": False
    },
    "moderator": {
        "borrow_book": False
    }
}

def has_permission(user: User, action: str) -> bool:
    return user_permissions.get(user.role, {}).get(action, False)

