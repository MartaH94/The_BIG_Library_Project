# class user to represent a user in te library or administrator

class User():
    def __init__(self, user_id, email, role="reader"):
        self.user_id = user_id
        self.email = email
        self.role = role

    def __repr__(self):
        return f"User id: {self.user_id}, user email: {self.email}, user role: {self.role}"