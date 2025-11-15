# functions to validate user's permissions 

from models.user import User

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

def has_permission(user: User, action: str) -> bool:
    return user_permissions.get(user.role, {}).get(action, False)

