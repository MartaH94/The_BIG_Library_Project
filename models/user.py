# class user to represent a user in te library or administrator

import exceptions as exc


valid_roles = ["reader", "admin"]
class User():
    def __init__(self, user_id, email, role="reader"):
        if role not in valid_roles:
            raise exc.UserInvalidRole
        self.user_id = user_id
        self.email = email
        self.role = role

    def __repr__(self):
        return f"User id: {self.user_id}, user email: {self.email}, user role: {self.role}"