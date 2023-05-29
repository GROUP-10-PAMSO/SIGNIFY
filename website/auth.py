from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from .models import SignatureModel
from .database import UserDatabase, SignDatabase

import os, pathlib, shutil

auth = Blueprint('auth', __name__)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        picture1 = request.files['picture1']
        picture2 = request.files['picture2']
        # toScanner = request.form.get('toScanner')
        
        # if toScanner:
        #     # Apply Scanner filter for the pictures
        #     pass
        
        # Get the file extensions of each pictures
        ext_picture1 = pathlib.Path(picture1.filename).suffix
        ext_picture2 = pathlib.Path(picture2.filename).suffix

        # Detect if one or all of the uploads were not existed or null
        if not picture1 or not picture2:
            pass
        
        # Making an if statement if the picture exists or supports the file format provided
        elif not(ext_picture1 in ALLOWED_EXTENSIONS) or not(ext_picture2 in ALLOWED_EXTENSIONS):
            pass

        elif picture1 and picture2: 

            # Outline for picture naming
            # userID_PictureNo

            picture1_sec = secure_filename(picture1.filename)
            picture2_sec = secure_filename(picture2.filename)

            # Not yet secured!!
            # Must be updated to detect if the directory is empty instead!!
            if not os.path.exists(UPLOAD_FOLDER + f"{current_user.id}/not sure") or not os.path.exists(UPLOAD_FOLDER + f"{current_user.id}/real") or not os.path.exists(UPLOAD_FOLDER + f"{current_user.id}/forg"):
                os.makedirs(UPLOAD_FOLDER + f"{current_user.id}/real")
                os.makedirs(UPLOAD_FOLDER + f"{current_user.id}/forg")
                os.makedirs(UPLOAD_FOLDER + f"{current_user.id}/not sure")
            
            user_folder = UPLOAD_FOLDER + f"{current_user.id}/not sure/"

            picture1.save(os.path.join(user_folder, picture1_sec))
            picture2.save(os.path.join(user_folder, picture2_sec))
            
            verify = SignatureModel(user_folder + picture1_sec, user_folder + picture2_sec)
            verify.preprocess()
            verify.predict()
            output = verify.output()

            verdict = output[0]
            percent = round(output[1][0] * 100, 2)

            counter = db.session.query(UserDatabase).filter(UserDatabase.id == current_user.id).first()
            counter.countPictures += 1
            db.session.commit()

            signVerified = SignDatabase(user_id=current_user.id, picture1=picture1_sec, picture2=picture2_sec, percentage=percent, isUserSignature=False)
            db.session.add(signVerified)
            db.session.commit()

            signID = db.session.query(SignDatabase.id).order_by(SignDatabase.id.desc()).first()[0]

            return redirect(url_for('output.result', signID=signID, verdict=verdict, percent=percent, picture1=picture1_sec, picture2=picture2_sec, isUserSignature=False))

    signCount = db.session.query(SignDatabase).count()
    meanAccuracy = db.session.query(db.func.avg(db.cast(SignDatabase.accurate, db.Integer))).filter(SignDatabase.accurate != None).scalar()
    if meanAccuracy:
        meanAccuracy = round(meanAccuracy * 100, 2)
    else:
        meanAccuracy = 0

    if current_user.is_anonymous:
        return redirect(url_for('auth.login'))
    else:
        return render_template("verify.html", user=current_user, signCount=signCount, meanAccuracy=meanAccuracy)

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