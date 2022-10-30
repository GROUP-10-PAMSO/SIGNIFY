from distutils.log import warn
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, UPLOAD_FOLDER
from .models import UserDatabase, SignatureModel

import os, pathlib

ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jfif', '.PNG']

auth = Blueprint('auth', __name__)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        picture1 = request.files['picture1']
        # picture2 = request.files['picture2']

        # Get the file extensions of each pictures
        ext_picture1 = pathlib.Path(picture1.filename).suffix
        # ext_picture2 = pathlib.Path(picture2.filename).suffix

        # Detect if one or all of the uploads were not existed or null
        if not picture1:
            pass
        
        # Making an if statement if the picture exists or supports the file format provided
        elif not(ext_picture1 in ALLOWED_EXTENSIONS):
            pass

        elif picture1: 

            # Outline for picture naming
            # PictureNo_userID

            picture1_sec = secure_filename(picture1.filename)
            # picture2_sec = secure_filename(picture2.filename)

            # Not yet secured!!
            picture1.save(os.path.join(UPLOAD_FOLDER, picture1_sec))

            # picture2.save(os.path.join(UPLOAD_FOLDER, picture2_sec)) 
            
            verify = SignatureModel(UPLOAD_FOLDER + picture1_sec)
            verify.preprocess()
            verify.predict()
            output = verify.output()

            result = output[0]
            percent = output[1]

            return render_template("verify.html", result=result, percent=percent, 
                picture1=picture1_sec, user=current_user)
                
    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    else:
        return render_template("verify.html", user=current_user)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = UserDatabase.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                print ("Went here 1")
                flash("Wrong email or password", category='error')
        else:
            flash("Wrong email or password", category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def signout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = UserDatabase.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exists", category='error')
        elif len(email) < 4:
            flash("Email must contain more than 4 characters!", category='error')
        elif len(username) < 2:
            flash("Username must be more than 2 characters!", category='error')
        elif password1 != password2:
            flash("Passwords don't match!", category='error')
        elif len(password1) < 6:
            flash("Passowrd must be more than 6 characters!", category='error')
        else:
            new_user = UserDatabase(email=email, username=username, countPictures=0, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        
    return render_template("signup.html", user=current_user)


