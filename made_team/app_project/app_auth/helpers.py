from flask_login import LoginManager
from models.models import ZmardAuthUsers, ZmardAuthRoles, ZmardAuthUserRoles

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    """Loads user, given the user_id."""
    logged_in_user = ZmardAuthUsers.query.get(int(user_id))
    return logged_in_user

# Other helper functions related to authentication here

# bcrypt is used to validating/hashing passwords
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
