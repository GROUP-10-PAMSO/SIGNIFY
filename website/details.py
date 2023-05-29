from flask import Blueprint, render_template, request, url_for, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename

from . import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from .database import UserDatabase, SignDatabase
from .models import SignatureModel

import os, pathlib, math

details = Blueprint('details', __name__)

@details.route('/account')
def account():
    return render_template("account.html", user=current_user)

@details.route('/viewDetails')
def viewDetails():
    return render_template("viewDetails.html", user=current_user)

@details.route('/changeSignature', methods=['POST'])
def changeSignature():
    userSignature = request.files['userSignature']
    ext_userSignature = pathlib.Path(userSignature.filename).suffix

    if not userSignature: # If the user didnt uploaded its new signature
        pass
    elif not(ext_userSignature in ALLOWED_EXTENSIONS): # If it is not a supported image file
        pass
    else:
        print(secure_filename(userSignature.filename))
        userSignature_sec = str(current_user.id) + "_userSignature.PNG"
        user_folder = UPLOAD_FOLDER + f"{current_user.id}/"
        userSignature.save(os.path.join(user_folder, userSignature_sec))

        change = db.session.query(UserDatabase).filter_by(id=current_user.id).first()
        change.signature = userSignature_sec
        db.session.commit()

        return jsonify(id=current_user.id ,userSignature_sec=userSignature_sec)

@details.route('/verifySignature', methods=['POST', 'GET'])
def verifySignature():
    toVerifySignature = request.files['verifySignature']
    ext_toVerifySignature = pathlib.Path(toVerifySignature.filename).suffix

    if not toVerifySignature: # If the user didnt uploaded the subjected signature
        pass
    elif not(ext_toVerifySignature in ALLOWED_EXTENSIONS): # If it is not a supported image file
        pass
    else:
        toVerifySignature_sec = secure_filename(toVerifySignature.filename)
        user_folder = UPLOAD_FOLDER + f"{current_user.id}/not sure/"
        toVerifySignature.save(os.path.join(user_folder, toVerifySignature_sec))
        
        userSignature = db.session.query(UserDatabase).filter_by(id=current_user.id).first()
        picture1 = userSignature.signature
        picture2 = toVerifySignature_sec
        
        verify = SignatureModel(UPLOAD_FOLDER + f"{current_user.id}/" + picture1, user_folder + picture2)
        verify.preprocess()
        verify.predict()
        output = verify.output()

        verdict = output[0]
        percent = round(output[1][0] * 100, 2)

        signVerified = SignDatabase(user_id=current_user.id, picture1=picture1, picture2=picture2, percentage=percent, isUserSignature=True)
        db.session.add(signVerified)
        db.session.commit()

        signID = db.session.query(SignDatabase.id).order_by(SignDatabase.id.desc()).first()[0]

        return jsonify({'redirect': url_for('output.result', signID=signID, verdict=verdict, percent=percent, picture1=picture1, picture2=picture2, isUserSignature=True)})


@details.route('/signatureCategory', methods=['POST'])
def signatureCategory():
    value = request.form.get('value')
    page = int(request.form.get('page'))
    itemLimit = 5
    start = (page - 1) * itemLimit

    totalRecords = db.session.query(SignDatabase).filter(db.and_(SignDatabase.user_id == current_user.id, SignDatabase.isUserSignature == value)).count()
    totalPages = 1 if (totalRecords == 0) else math.ceil(totalRecords / itemLimit)

    getSignatures = db.session.query(SignDatabase).filter(db.and_(SignDatabase.user_id == current_user.id, SignDatabase.isUserSignature == value)).offset(start).limit(itemLimit).all()
    listSignatures = [(row.id, row.picture1, row.picture2, row.percentage, row.accurate, row.date) for row in getSignatures]

    return jsonify(listSignatures=listSignatures, totalPages=totalPages, totalRecords=totalRecords, start=start)

@details.route('/moreDetails', methods=['POST'])
def moreDetails():
    signID = request.form.get('signID')

    getRecord = SignDatabase.query.get_or_404(signID)

    boolPercentage = True if getRecord.percentage <= 50 else False
    prediction = int(boolPercentage if getRecord.accurate else ((not boolPercentage) if getRecord.accurate != None else 2))
    confirmed = True if prediction != 2 else False
    
    verdict = "Genuine" if (getRecord.percentage <= 0.5) else "Forged"

    return jsonify({'redirect': url_for('output.result', verdict=verdict, percent=getRecord.percentage, picture1=getRecord.picture1, picture2=getRecord.picture2, isUserSignature=getRecord.isUserSignature, confirmed=confirmed, prediction=prediction, signID=signID)})