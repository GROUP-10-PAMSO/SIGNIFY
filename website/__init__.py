from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

UPLOAD_FOLDER = 'website/static/sign_storage/'
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jfif', '.PNG']

def create_app():
	app = Flask(__name__) #initializes the app
	app.config['SECRET_KEY'] = 'signify10' #encrypts or secure the cookies or session data
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
	db.init_app(app)

	from .views import views
	from .auth import auth
	from .details import details

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')
	app.register_blueprint(details, url_prefix='/')

	from .database import UserDatabase
	
	# Creates an external database
	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(id):
		return UserDatabase.query.get(int(id))

	return app

def create_database(app):
	# Checks if the database is created already. If not, create a new one.
	if not path.exists('instance/' + DB_NAME):
		with app.app_context():
			db.create_all()