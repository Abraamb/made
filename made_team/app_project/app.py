#https://www.digitalocean.com/community/tutorials/how-to-structure-a-large-flask-application-with-flask-blueprints-and-flask-sqlalchemy
# We used this link for the bp and the db connection/tabels  
from flask import Flask, render_template

from config import Config
from extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config['SECRET_KEY'] = 'your_secret_key' 

    # [1/2] Start Authentication (import this before db is initialized)
    # Adding the authentication database to the alchemy-binds
    app.config['SQLALCHEMY_BINDS'] = {
    "auth": {
        "url" : 'mysql://u155771p146127_readonly:iuwG6N30EF@185.104.29.144/u155771p146127_zmardusers',
        "pool_recycle" : 280,
        "pool_pre_ping" : True
        }
    }
    # [1/2] End Authentication

    
    # Initialize Flask extensions here
    db.init_app(app)
    
    # [2/2] Start Authentication (import this after db is initialized)
    from app_auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth') # registers auth blueprint
  
    from app_auth.helpers import login_manager
    login_manager.init_app(app) # initializes login_manager
    login_manager.login_view = 'auth.login' # sets the login view to the login page
    # [2/2] End Authentication
    
    # blueprints here
    from main import bp as main_bp
    app.register_blueprint(main_bp)

    from app_abraam import bp as abraam_bp
    app.register_blueprint(abraam_bp, url_prefix='/abraam')

    from app_lars import bp as lars_bp 
    app.register_blueprint(lars_bp, url_prefix='/lars')

    from app_jay import bp as jay_bp 
    app.register_blueprint(jay_bp, url_prefix='/jay')
    
    return app

app = create_app(Config)
