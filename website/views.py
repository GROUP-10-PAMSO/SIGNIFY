from flask import Blueprint, render_template, request
from flask_login import current_user

from skimage.filters import threshold_local
from werkzeug.utils import secure_filename
import cv2, os

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Temporary Placeholder
    return render_template("index.html", user=current_user)

@views.route('/aboutus')
def aboutus():
    return render_template("aboutus.html", user=current_user)

@views.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        picture = request.files['picture1']

        picture_sec = secure_filename(picture.filename)
        picture.save(os.path.join("website", picture_sec))

        picture1 = cv2.imread("website/" + picture_sec, cv2.IMREAD_GRAYSCALE)
        picture1 = cv2.resize(picture1, (640, 480))

        cv2.imshow("Before Image", picture1)
        T = threshold_local(picture1, 11, offset = 10, method = "gaussian")
        picture1 = (picture1 > T).astype("uint8") * 255

        cv2.imshow("After Image", picture1)
        cv2.waitKey(0)  

    return render_template("test.html", user=current_user)
