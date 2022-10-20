from flask import Flask
# from keras.models import load_model

# Not usable as of now
UPLOAD_FOLDER = 'website/static/sign_storage/'

def create_app():
	app = Flask(__name__) #initializes the app
	app.config['SECRET_KEY'] = 'signify10' #encrypts or secure the cookies or session data
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	return app
