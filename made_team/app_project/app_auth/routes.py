from flask import render_template, request, redirect, url_for, flash
from app_auth import bp
from models.models import ZmardAuthUsers
from .helpers import bcrypt
from flask import session
from flask_login import login_user, logout_user
from flask_login import login_required, current_user
import re


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # check if the user exists in the database
        user = ZmardAuthUsers.query.filter_by(email=email).first()

        # check whether ther user exists and is activated
        if user and user.activated == False:
            flash("Your account is not activated.")
            return redirect(url_for("auth.login"))

        # if the user exists, then check if the password is correct
        if user and bcrypt.check_password_hash(user.password, password) and user.activated == True:
            # password is correct, so login the user
            login_user(user)
            # if "next" in request arguments is found, redirect to that page,
            # otherwise redirect to main which we assume is "/" due to the nature this code is used
            # in normal environments, we would use url_for("main.index") instead (or whatever the main page is)
            
            next_page = request.args.get("next")
            # disabled the next_page feature for now due to vulnerability: Open Redirects
            #return redirect(next_page) if next_page else redirect('/')
            return redirect('/') 
        else:
            # password is incorrect, so show an error message
            flash("Login unsuccessful. Please check email and password.")
            return redirect(url_for("auth.login"))
    

    return render_template("zmard_dashboard/login.html")

@bp.route("/logout", methods=["GET"])
def logout():
    # logout the user
    logout_user()
    # redirect to the login page
    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    enabled = False
    if enabled != True:
        flash("Registration is currently disabled. Don't have an account? Contact zmard.")
        return redirect(url_for("auth.login"))
    
    # if the request is a POST request, then try to register the user
    if request.method == "POST" and enabled == True:
        firstName = request.form.get("firstName")
        lastName = request.form.get("lastName")
        email = request.form.get("email")
        password = request.form.get("password")

        # check if this account already exists
        user_exists = ZmardAuthUsers.query.filter_by(email=email).first()
        if user_exists:
            flash("This email is already registered. Please login.")
            return redirect(url_for("auth.login"))
        
        # check if the email is valid
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash("Please enter a valid email address")
            return redirect(url_for("auth.register"))

        # check if the password meets the requirements
        if not re.search(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$', password):
            flash("Password must be at least 8 characters long and contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character (!@#$%^&*)")
            return redirect(url_for("auth.register"))        

        #======================
        # Create a new uwer
        #======================
        # 1. Hash the password using bcrypt
        password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
        # 2. Create a new user object
        new_user = ZmardAuthUsers(
            firstName=firstName,
            lastName=lastName,
            email=email,
            password=password_hash)
        
        from core.extensions import db
        # 3. Add the new user to the database
        if db:
            db.session.add(new_user)
            db.session.commit()

            flash("Account created successfully. Please login.")
            return redirect(url_for("auth.login"))
        return 'registration not available'
    
    
    # If the request is a GET request, then just render the register page
    return render_template("zmard_dashboard/register.html")
