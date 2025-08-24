# managing registration, login, and authorisation of users
from models.user import User
import exceptions as exc
from utils.validators import has_permission

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