from flask import Blueprint, render_template, request, flash
from flask_login import current_user
from requests import Session
from sqlalchemy import select, engine

from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # Temporary Placeholder
    return render_template("index.html", user=current_user)

@views.route('/aboutus')
def aboutus():
    return render_template("aboutus.html", user=current_user)
