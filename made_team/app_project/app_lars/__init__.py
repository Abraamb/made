from flask import Blueprint

bp = Blueprint('lars', __name__)

from app_lars import routes
