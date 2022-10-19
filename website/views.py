from flask import Blueprint, render_template, request, flash

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Temporary Placeholder
    return render_template("index.html")