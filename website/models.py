import numpy as np
import cv2

from keras.models import load_model
from keras.layers import Lambda
from keras import layers
from keras import Input
from keras import regularizers
import tensorflow as tf

SIZE = 128

def euclidean_distance(vects):
    x, y = vects
    sum_square = tf.math.reduce_sum(tf.math.square(x - y), axis=1, keepdims=True)
    return tf.math.sqrt(tf.math.maximum(sum_square, tf.keras.backend.epsilon()))

def architecture(weights): 
    input = layers.Input((128, 128, 1))
    x = tf.keras.layers.BatchNormalization()(input)
    x = layers.Conv2D(32, (5, 5), activation="relu",kernel_regularizer=regularizers.L2(l2=2e-4),
        bias_regularizer=regularizers.L2(2e-4))(x)
    x = layers.AveragePooling2D(pool_size=(2, 2))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Conv2D(32, (5, 5),kernel_regularizer=regularizers.L1L2(l1=1e-5, l2=1e-4),
        bias_regularizer=regularizers.L2(2e-4), activation="relu")(x)
    x = layers.AveragePooling2D(pool_size=(2, 2))(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Flatten()(x)

    x = tf.keras.layers.BatchNormalization()(x)
    x = layers.Dense(128, activation="relu")(x)
    embedding_network = tf.keras.Model(input, x)

    input_1 = layers.Input((128, 128, 1))
    input_2 = layers.Input((128, 128, 1))

    # As mentioned above, Siamese Network share weights between
    # tower networks (sister networks). To allow this, we will use
    # same embedding network for both tower networks.
    tower_1 = embedding_network(input_1)
    tower_2 = embedding_network(input_2)

    merge_layer = layers.Lambda(euclidean_distance)([tower_1, tower_2])
    normal_layer = tf.keras.layers.BatchNormalization()(merge_layer)
    output_layer = layers.Dense(1, activation="sigmoid")(normal_layer)
    siamese = tf.keras.Model(inputs=[input_1, input_2], outputs=output_layer)
    siamese.compile(loss='binary_crossentropy', optimizer="adam", metrics=["accuracy"])
    siamese.load_weights(weights)

    return siamese
    
class SignatureModel:
    def __init__(self, picture1, picture2):
        self.picture1 = picture1
        self.picture2 = picture2

        self.result = ""
        self.percentage = ""

        self.model = architecture("website/static/siamese_model1.h5")
    
    # Resizing the pictures
    def preprocess(self):
        self.picture1 = cv2.imread(self.picture1, cv2.IMREAD_GRAYSCALE)
        self.picture1 = cv2.resize(self.picture1, (SIZE, SIZE))

        self.picture2 = cv2.imread(self.picture2, cv2.IMREAD_GRAYSCALE)
        self.picture2 = cv2.resize(self.picture2, (SIZE, SIZE))
    
    # Comparing the two pictures if they are similar in terms of similarities in signature
    # It will use the json model from the custom machine learning model made from the verificator folder
    def predict(self):
        prediction = self.model.predict([self.picture1.reshape((1, 128, 128)), self.picture2.reshape((1, 128, 128))])

        if prediction <= 0.5:
            self.result = "Genuine"
        else:
            self.result = "Forged"

        self.percentage = prediction[0]

    # Returns the result and its percentage
    def output(self):
        return self.result, self.percentage