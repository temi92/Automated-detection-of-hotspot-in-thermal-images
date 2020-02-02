from flask import Flask, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sklearn.preprocessing import LabelEncoder
from PIL import Image, ImageDraw, ImageFont
from hotspotDetection import Roi
import tensorflow as tf
import pickle
import numpy as np
import io
import base64
import cStringIO
import cv2
import os
import config
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
#print ("sqlite:///"+os.path.join(basedir, "tmp.sqlite"))

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(basedir, "tmp.sqlite")
app.config.from_object(os.environ["APP_SETTINGS"])

app.config[" SQLALCHEMY_TRACK_MODIFICATIONS "] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Image(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    data = db.Column(db.LargeBinary)

#model to extract features from image
#model_vgg16 = tf.keras.applications.VGG16(weights="imagenet", include_top=False)
model_vgg16 = tf.keras.models.load_model("hotspotDetection/vgg16.h5")
#model to run classifier on extracted features.
model = None

l = LabelEncoder()


def load_model():
    with open("hotspotDetection/model.cpickle", 'rb') as f:
        global model
        model = pickle.load(f)

def preprocess_image(file_image, image_size):
    #convert to numpy array
    image = tf.keras.preprocessing.image.load_img(file_image, target_size=image_size)
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = tf.keras.applications.imagenet_utils.preprocess_input(image)
    return image

def preprocess_cvimg(image, image_size):
    cv_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(cv_image)

    im_resized = pil_image.resize(image_size)
    img_array = tf.keras.preprocessing.image.img_to_array(im_resized)
    img_array = np.expand_dims(img_array,axis=0)

    img_array = tf.keras.applications.imagenet_utils.preprocess_input(img_array)
    return img_array

    
def get_byte_image(image):
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

def label_image(image, text):
    cv2.putText(image, "Label: {}".format(text),
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

load_model()
@app.route("/")
@app.route("/predict_image", methods=["GET", "POST"])
def predict_image():
    if request.method == "POST":
        file_image = request.files["file_image"]

        #get image in opencv format..
        image = cv2.imdecode(np.fromstring(request.files['file_image'].read(), np.uint8), cv2.IMREAD_UNCHANGED)

        # pass file_object to keras api backend..
        img = preprocess_image(file_image, (224,224))
        
        #extract features using VGG16 model..
        preds = model_vgg16.predict(img)
        preds = preds.reshape((preds.shape[0], 512 * 7 * 7))
        #use logistic regression model to get prediction from features.
        pred_label = model.predict(preds)[0]
        prob = model.predict_proba(preds)

        if pred_label == 0:
            label = "Hotspot"
            roi = Roi(image)
            image = roi.get_roi()
        else:
            label = "No Hotspot"

    
        label_image(image, label)

        #encode image to send to backend.
        encoded_image = get_byte_image(image)
        return jsonify({"encoded_img":encoded_image, "hotspot_prob": prob[0][0], "nohotspot_prob":prob[0][1]})
        
    return render_template("index.html")

@app.route("/misclassified_image", methods=["POST"])
def misclassified_image():
    file_image = request.files["misclassified_image"]
    print(file_image.filename)
    image = Image(name=file_image.filename,data=file_image.read())
    db.session.add(image)
    db.session.commit()
    return jsonify({"success":file_image.filename})


if __name__ == '__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
