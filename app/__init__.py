from flask import Flask
from config import config_options
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_mail import Mail
from flask_simplemde import SimpleMDE
from flask_migrate import Migrate
import os


bootstrap = Bootstrap()
db = SQLAlchemy()
# migrate = Migrate()
mail = Mail()
simple = SimpleMDE()
photos = UploadSet('photos', IMAGES) #UPLOAD SET DEFINES WHAT WE ARE UPLOADING, we pass in a name and the type of file we want to upload which is an image
login_manager = LoginManager() #create an instance 
login_manager.session_protection = 'strong' #provides diff security levels and by using strong it will minitor changes in the user header and log the user out
login_manager.login_view = 'auth.login' #add the blueprint name as the login endpoint as it is located inside a blueprint

def create_app(config_name):
    app = Flask(__name__)
    # app.config['SESSION_TYPE'] = 'memcached'
    # app.config['SECRET_KEY'] = 'super secret key'
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY
    
    app.config.from_object(config_options[config_name])

    configure_uploads(app, photos)

    bootstrap.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    mail.init_app(app)
    login_manager.init_app(app)
    simple.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/authenticate')

    # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL").replace('postgres://', 'postgresql://')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    return app