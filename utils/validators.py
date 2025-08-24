# functions to validate user inputs, eg. login, credentials, etc.

from models.user import User

user_permissions = {
    "reader" : {
        "borrow_book" : True,
        "return_book" : True,
        "view_books" : True,
        "manage_books" : False,
        "manage_users" : False
    },
    "admin": {
        "borrow_book" : False,
        "return_book" : False,
        "view_books" : True,
        "manage_books" : True,
        "manage_users" : True
    }
}

def has_permission(user, action):
    role = user.role
    return user_permissions.get(role, {}).get(action, False)

