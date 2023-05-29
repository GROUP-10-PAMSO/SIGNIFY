from flask import Blueprint, render_template, request
from flask_login import current_user
from . import db, UPLOAD_FOLDER
from .database import SignDatabase

import shutil

output = Blueprint('output', __name__)

@output.route('/result', methods=['GET', 'POST'])
def result():
    signID = int(request.args.get('signID'))
    isUserSignature = (request.args.get('isUserSignature') == 'True')
    percentage = float(request.args.get('percent'))
    picture1 = request.args.get('picture1')
    picture2 = request.args.get('picture2')

    confirmed = request.args.get('confirmed')
    confirmed = (confirmed == 'True') if confirmed else False

    prediction = request.args.get('prediction')
    prediction = int(prediction) if prediction else 2

    if request.method == "POST":
        if current_user.is_authenticated:
            confirmation = int(request.form['confirmation'])
            signID = int(request.form['signID'])

            if isUserSignature:
                return ownSignature(confirmation, percentage, picture2, signID)
            else:
                return otherSignature(confirmation, percentage, picture1, picture2, signID)

    return toDatabase(prediction, isUserSignature, confirmed, signID)

def ownSignature(confirmation, percentage, picture2, signID):
    # Will send to SignDatabase if the signature detected is accurate
    # Disregards the "not sure" data but it would still count on the number of signatures verified
    prediction = 1 if percentage <= 50 else 0
    if confirmation == 0: # Yes
        SignDatabase.query.filter_by(id=signID).update({SignDatabase.accurate: True})
        db.session.commit()
        if prediction == 1:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture2}")
        elif prediction == 0:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture2}")
    elif confirmation == 1: # No
        SignDatabase.query.filter_by(id=signID).update({SignDatabase.accurate: False})
        db.session.commit()
        prediction = not prediction
        if prediction == 1:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture2}")
        elif prediction == 0:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture2}")
    elif confirmation == 2: # Not Sure
        prediction = 2

    return toDatabase(prediction, True, True)

def otherSignature(confirmation, percentage, picture1, picture2, signID):
    # Will send to SignDatabase if the signature detected is accurate
    # Disregards the "not sure" data but it would still count on the number of signatures verified
    prediction = 1 if percentage <= 50 else 0
    if confirmation == 0: # Yes
        SignDatabase.query.filter_by(id=signID).update({SignDatabase.accurate: True})
        db.session.commit()
        if prediction == 1:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture1}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture1}")
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture2}")
        elif prediction == 0:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture1}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture1}")
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture2}")
    elif confirmation == 1: # No
        SignDatabase.query.filter_by(id=signID).update({SignDatabase.accurate: False})
        db.session.commit()
        prediction = not prediction
        if prediction == 1:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture1}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture1}")
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/real/{picture2}")
        elif prediction == 0:
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture1}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture1}")
            shutil.move(UPLOAD_FOLDER + f"{current_user.id}/not sure/{picture2}", UPLOAD_FOLDER + f"{current_user.id}/forg/{picture2}")
    elif confirmation == 2: # Not Sure
        prediction = 2

    return toDatabase(prediction, False, True)

def toDatabase(prediction, isUserSignature, confirmed, signID=None):
    signCount = db.session.query(SignDatabase).count()
    meanAccuracy = db.session.query(db.func.avg(db.cast(SignDatabase.accurate, db.Integer))).filter(SignDatabase.accurate != None).scalar()
    if meanAccuracy:
        meanAccuracy = round(meanAccuracy * 100, 2)
    else:
        meanAccuracy = 0

    return render_template("result.html", user=current_user, 
        verdict=request.args.get('verdict'), percent=request.args.get('percent'),
        picture1=request.args.get('picture1'),
        picture2=request.args.get('picture2'), confirmed=confirmed, prediction=prediction,
        signCount=signCount, meanAccuracy=meanAccuracy, isUserSignature=isUserSignature, signID=signID)