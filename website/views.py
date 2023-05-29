from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Temporary Placeholder
    return render_template("index.html", user=current_user)

@views.route('/aboutus')
def aboutus():
    return render_template("aboutus.html", user=current_user)
