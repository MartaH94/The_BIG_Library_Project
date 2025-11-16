# class user to represent a user in te library or administrator
""" This module defines the User class for representing users in the library management system.
    """

import exceptions as exc


valid_roles = ["reader", "admin", "librarian", "guest", "moderator"]
class User():
    def __init__(
            self,
            user_id,
            email,
            role,
            user_name = None,
            first_name = None,
            last_name = None,
            phone_number = None,
            password_hash = None,
            is_active = None,
            last_login = None
    ):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.password_hash = password_hash
        self.is_active = is_active
        self.last_login = last_login

        if self.role not in valid_roles:
            raise exc.UserInvalidRole(f"The {role} is not available.")
        
        

    def __repr__(self):
        return f"User id: {self.user_id}, user email: {self.email}, user role: {self.role}"
    

    