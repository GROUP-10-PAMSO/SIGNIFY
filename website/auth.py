from inspect import Signature
from flask import Blueprint, render_template, request, flash
from .models import SignatureModel

auth = Blueprint('auth', __name__)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        picture1 = "Image"
        picture2 = "Image"
  
        verify = SignatureModel(picture1, picture2)
        # verify.preprocess()
        verify.testing()
        output = verify.output()

        result = output[0]
        percent = output[1]

        return render_template("verify.html", result=result, percent=percent)

    return render_template("verify.html")