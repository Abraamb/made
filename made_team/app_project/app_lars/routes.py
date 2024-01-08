from flask import render_template, url_for
from app_lars import bp
from flask_login import login_required, current_user



@bp.route('/settings/')
def settings(): 
    return render_template('settings/settings.html')