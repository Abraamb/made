from flask import render_template, request, url_for, redirect
from main import bp
from extensions import db
from models.voorwerpen import Voorwerpen
from flask import Flask, render_template, request, session
from flask_login import login_required, current_user

@bp.route('/')
# Restricting access to authenticated users only
@login_required
def start():
    # Getting the roles of the current user
    roles = str([user_role.role for user_role in current_user.roles])
    return render_template('start.html', roles=roles)




