import cv2

size = 224
class SignatureModel:
    def __init__(self, picture1, picture2):
        self.picture1 = picture1
        self.picture2 = picture2
        self.result = ""
        self.percentage = ""

    # Resizing the pictures
    def preprocess(self):
        self.picture1 = cv2.imread(self.picture1, cv2.COLOR_BGR2RGB)
        self.picture1 = cv2.resize(self.picture1, (size, size))

        self.picture2 = cv2.imread(self.picture2, cv2.COLOR_BGR2RGB)
        self.picture2 = cv2.resize(self.picture2, (size, size))
    
    # Comparing the two pictures if they are similar in terms of similarities in signature
    # It will use the json model from the custom machine learning model made from the verificator folder
    def testing(self):
        # Testing process...
        self.result = "Placeholder"
        self.percentage = "NaN%"

    # Returns the result and its percentage
    def output(self):
        return self.result, self.percentage