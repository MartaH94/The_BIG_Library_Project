# managing registration, login, and authorisation of users

from models.user import User
import exceptions as exc



user_permissions = {
    "reader" : {
        "books": {
            "borrow_book" : True,
            "return_book" : True,
            "reserve_book" : True,
            "add_book" : False,
            "edit_book" : False,
            "delete_book" : False,
            "search_book" : True,
            "view_books" : True
        },

        "account": {
            "update_account": False,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True
        },

        "actions": {
            "approve_reservations": False,
            "manage_users" : False,
            "view_logs": False,
            "generate_reports": False,
            "delegate_permissions": False,
            "delete_data" : False,
            "edit_data" : False
        }
    },

    "admin": {
        "books": {
            "borrow_book" : False,
            "return_book" : False,
            "reserve_book" : True,
            "add_book" : True,
            "edit_book" : True,
            "delete_book" : True,
            "search_book" : True,
            "view_books" : True
        },

        "account": {
            "update_account": True,
            "update_own_data": True,
            "reset_password": True,
            "view_borrow_history": True
        },

        "actions": {
            "approve_reservations": False,
            "manage_users" : True,
            "view_logs": True,
            "generate_reports": True,
            "delegate_permissions": True,
            "delete_data" : True,
            "edit_data" : True
        }    
    },

    "librarian": {
        "books": {
            "borrow_book" : False,
            "return_book" : False,
            "reserve_book" : True,
            "add_book" : True,
            "edit_book" : True,
            "delete_book" : True,
            "search_book" : True,
            "view_books" : True
        },

        "account": {
            "update_account": True,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True
        },

        "actions": {
            "approve_reservations": True,
            "manage_users" : False,
            "view_logs": False,
            "generate_reports": True,
            "delegate_permissions": False,
            "delete_data" : True,
            "edit_data" : True
        }
    },

    "guest": {
        "books": {
            "borrow_book" : False,
            "return_book" : False,
            "reserve_book" : True,
            "add_book" : False,
            "edit_book" : False,
            "delete_book" : False,
            "search_book" : True,
            "view_books" : True
        },

        "account": {
            "update_account": False,
            "update_own_data": False,
            "reset_password": False,
            "view_borrow_history": False
        },

        "actions": {
            "approve_reservations": False,
            "manage_users" : False,
            "view_logs": False,
            "generate_reports": False,
            "delegate_permissions": False,
            "delete_data" : False,
            "edit_data" : False
        }
    },

    "moderator": {
        "books": {
            "borrow_book" : False,
            "return_book" : False,
            "reserve_book" : False,
            "add_book" : True,
            "edit_book" : True,
            "delete_book" : False,
            "search_book" : True,
            "view_books" : True
        },

        "account": {
            "update_account": False,
            "update_own_data": True,
            "reset_password": False,
            "view_borrow_history": True
        },

        "actions": {
            "approve_reservations": False,
            "manage_users" : False,
            "view_logs": True,
            "generate_reports": True,
            "delegate_permissions": False,
            "delete_data" : False,
            "edit_data" : True
        }
    }
}

def has_permission(role: str, action_path: str) -> bool:
    """This function checks if a specific role has permission to perform a specific action.

    Args:
        role (str): The role name (e.g., "admin", "reader").
        action_path (str): Dot-separated path to the permission (e.g., "books.borrow_book").

    Returns:
        bool: True if the role has permission, False otherwise.
    """
    permissions = user_permissions.get(role, {})
    keys = action_path.split(".")
    for key in keys:
        if not isinstance(permissions, dict):
            return False
        permissions = permissions.get(key, None)
        if permissions is None:
            return False
    return bool(permissions)
    




class UserAuthorisation():
    def __init__(self):
        self.logged_in_user = None

    def login(self, user: User):
        self.logged_in_user = user

    def logout(self):
        self.logged_in_user = None
    
    def check_permission(self, action):
        if not self.logged_in_user:
            raise exc.PermissionError("No logged in user.")
        if not has_permission(self.logged_in_user, action):
            raise exc.PermissionError(f"User: {self.logged_in_user.role} cannot perform action '{action}'")
        
        return True