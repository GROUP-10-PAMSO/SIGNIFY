from flask import Flask #initialize Flask


def create_app():
	app = Flask(__name__) #initializes the app
	app.config['SECRET_KEY'] = 'signify10' #encrypts or secure the cookies or session data

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	return app
