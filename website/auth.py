from flask import Blueprint, render_template, request, flash, current_app
from werkzeug.utils import secure_filename

from . import UPLOAD_FOLDER
from .models import SignatureModel
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
                picture1=picture1_sec)
                
    return render_template("verify.html")