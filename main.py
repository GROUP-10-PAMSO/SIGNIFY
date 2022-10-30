from website import create_app

app = create_app()

if __name__ == '__main__': # runs the webserver only if the app is open
	app.run(debug=True) # automatically rerun the app if there is changes