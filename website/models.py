from keras.models import load_model
from flask_login import UserMixin
from . import db

import numpy as np
import cv2

SIZE = 224
class SignatureModel:
    def __init__(self, picture1):
        self.picture1 = picture1
        # self.picture2 = picture2

        self.result = ""
        self.percentage = ""

        self.model = load_model('website/static/ver1_mobilenetv2.h5')

    # Resizing the pictures
    def preprocess(self):
        self.picture1 = cv2.imread(self.picture1)
        self.picture1 = cv2.cvtColor(self.picture1, cv2.COLOR_BGR2RGB)
        self.picture1 = cv2.resize(self.picture1, (SIZE, SIZE))
        self.picture1 = np.expand_dims(self.picture1, axis=0)

        # data2 = cv2.imread(self.picture2, cv2.COLOR_BGR2RGB)
        # data2 = cv2.cvtColor(data2, cv2.COLOR_BGR2RGB)
        # data2 = cv2.resize(self.picture2, (SIZE, SIZE))
    
    # Comparing the two pictures if they are similar in terms of similarities in signature
    # It will use the json model from the custom machine learning model made from the verificator folder
    def predict(self):
        prediction = self.model.predict(self.picture1)

        self.result = "Placeholder"
        self.percentage = prediction[0][0]

    # Returns the result and its percentage
    def output(self):
        return self.result, self.percentage

class UserDatabase(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    countPictures = db.Column(db.Integer)
    password = db.Column(db.String(150))