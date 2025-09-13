# functions to validate user inputs, eg. login, credentials, etc.

from models.user import User

user_permissions = {
    "reader" : {
        "borrow_book" : True,
        "return_book" : True,
        "book_the_book" : True,
        "view_books" : True,
        "add_book" : True,
        "edit_book" : False,
        "delete_book" : False,
        "search_book" : True,
        "manage_users" : False
    },
    "admin": {
        "borrow_book" : False,
        "return_book" : False,
        "book_the_book" : False,
        "view_books" : True,
        "add_book" : True,
        "edit_book" : True,
        "delete_book" : True,
        "search_book" : True,
        "manage_users" : True
    }
}

def has_permission(user: User, action: str) -> bool:
    return user_permissions.get(user.role, {}).get(action, False)

