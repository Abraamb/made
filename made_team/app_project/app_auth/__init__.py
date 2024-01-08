# ============================================================
# ZMARD Authentication Module
# Author: Roy Zonneveld
# ============================================================
#
# This module was developed by Roy, designed for teams working on ZMARD projects,
# and is designed for handling user authentication within various applications.
#
# Before implementing this module into your application:
# 1. Review the structure and schema of the database models (Users, Roles, UserRoles)
#    to ensure they match your application's requirements.

# NOTE TO SELF: 
# 1. Secret_key must be valid
# 2. look into whether mysqlalchemy is imported (and used, otherwise, alchemy needs to be imported)

# blueprints can be protected by using the @login_required decorator, see own project as example (might be useful for documentation)


from flask import Blueprint

bp = Blueprint('auth', __name__)

from app_auth import routes
