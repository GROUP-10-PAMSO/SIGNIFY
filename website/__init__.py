from flask import FLask #initialize Flask

def create_app():
	app = FLask(__name__) #initializes the app
	app.config['SECRET_KEY'] = 'signify10' #encrypts or secure the cookies or session data

	return app
