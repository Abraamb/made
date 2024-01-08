# Explainaition of the database structure, and how it's used
# 
# The database structure is as follows:
# 
# This model includes the following tables:
# 1. users
# 2. roles
# 3. user_roles
#
# This model is used to authenticate users, and to assign roles to users. Which can be used to determine what a user can do.
#
# Here are a few examples of how this model works when creating/modifying entries:
#
# 1. Create a new user:
# new_user = ZmardAuthUsers(firstName="John", lastName="Doe", email="john.doe@example.com", password="secure_password")
# db.session.add(new_user)
# db.session.commit()
#
# 2. Create a new role:
# new_role = ZmardAuthRoles(name="admin", description="Administrator role with full permissions")
# db.session.add(new_role)
# db.session.commit()
#
# 3. Assign a role to a user:
# user = ZmardAuthUsers.query.filter_by(email="john.doe@example.com").first()
# role = ZmardAuthRoles.query.filter_by(name="admin").first()
# user_rol = ZmardAuthUserRoles(user_id=user.id, role_id=role.id)
# db.session.add(user_rol)
# db.session.commit()
#
# 4. Query all users with specific role:
# admin_role = ZmardAuthRoles.query.filter_by(name="admin").first()
# admin_users = [user_role.user for user_role in admin_role.users]
#
# 5. Query all roles assigned to a specific user:
# user = ZmardAuthUsers.query.filter_by(email="john.doe@example.com").first()
# all roles: user.roles, so you can do:
# user_roles = [user_role.role for user_role in user.roles]
#
# 6. Remove a role from a user:
# user = ZmardAuthUsers.query.filter_by(email="john.doe@example.com").first()
# role = ZmardAuthRoles.query.filter_by(name="admin").first()
# user_role = ZmardAuthUserRoles.query.filter_by(user_id=user.id, role_id=role.id).first()
# db.session.delete(user_role)
# db.session.commit()
#
# 7. Update a user's information:
# user = ZmardAuthUsers.query.filter_by(email="john.doe@example.com").first()
# user.email = "john.doe_new@example.com"
# db.session.commit()


# SQL Alchemy
try:
    from ..app import db
except:
    pass
try:
    from .. import db
except:
    pass
try:
    from extensions import db
except:
    pass
try:
    from ..wsgi import db
except:
    pass

from flask_login import UserMixin

class ZmardAuthUsers(db.Model, UserMixin):
    """User model for authentication."""

    __bind_key__ = "auth"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(128), nullable=False)
    lastName = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    activated = db.Column(db.Boolean(), default=True, nullable=False)

    # automatic timestamps
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # Define the relationship to the RoleUser model
    roles = db.relationship('ZmardAuthUserRoles', back_populates='user')

    def __repr__(self):
        return f"User(#{self.id} - {self.email})"

class ZmardAuthRoles(db.Model):
    """Role model for defining user permissions."""

    __bind_key__ = "auth"
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Define the relationship to the RoleUser model
    users = db.relationship('ZmardAuthUserRoles', back_populates='role')

    def __repr__(self):
        return f"Role('#{self.id} - {self.name}')"

class ZmardAuthUserRoles(db.Model):
    """Association table between Users and Roles."""

    __bind_key__ = "auth"
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    user = db.relationship('ZmardAuthUsers', back_populates='roles')
    role = db.relationship('ZmardAuthRoles', back_populates='users')

    def __repr__(self):
        return f"UserRoles('#{self.user_id}'-'{self.user.firstName}', '{self.role.name}')"