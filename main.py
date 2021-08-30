from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request
import numpy as np
import tensorflow

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename

import sys
import os
import glob
import re


from flask import send_from_directory
import tensorflow as tf

from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image



app = Flask(__name__, template_folder='templates')

MODEL_PATH ='malaria_model.h5'
model = load_model(MODEL_PATH)

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(224, 224))

    # Preprocessing the image
    x = image.img_to_array(img)
    # x = np.true_divide(x, 255)
    ## Scaling
    x=x/255
    x = np.expand_dims(x, axis=0)
   

    # Be careful how your trained model deals with the input
    # otherwise, it won't make correct prediction!
    x = preprocess_input(x)

    preds = model.predict(x)
    preds=np.argmax(preds, axis=1)
    if preds==0:
        preds="Sorry you have high chances of getting the disease. Please consult the doctor immediately"
    else:
        preds="No need to fear. You have no dangerous symptoms of the disease."
    
    
    return preds

@app.route('/malaria', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/malariaprediction', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        result1=preds
        return result1




@app.route("/")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/cancer")
def cancer():
    return render_template("cancer.html")


@app.route("/diabetes")
def diabetes():
    #if form.validate_on_submit():
    return render_template("diabetes.html")

@app.route("/heart")
def heart():
    return render_template("heart.html")


@app.route("/liver")
def liver():
    #if form.validate_on_submit():
    return render_template("liver.html")

@app.route("/kidney")
def kidney():
    #if form.validate_on_submit():
    return render_template("kidney.html")






def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==5):
        loaded_model = joblib.load('cancer_model.pkl')
        result = loaded_model.predict(to_predict)
    elif(size==6):
        loaded_model = joblib.load('diabetes_model.pkl')
        result = loaded_model.predict(to_predict)
    elif(size==4):
        loaded_model = joblib.load('heart_model.pkl')
        result = loaded_model.predict(to_predict)
    elif(size==8):
        loaded_model = joblib.load('kidney_model.pkl')
        result = loaded_model.predict(to_predict)
    elif(size==7):
        loaded_model = joblib.load('liver_model.pkl')
        result = loaded_model.predict(to_predict)   
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    result=0;
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
         #cancer
        if(len(to_predict_list)==5):
            result = ValuePredictor(to_predict_list,5)
        elif(len(to_predict_list)==6):
            result = ValuePredictor(to_predict_list,6)
        elif(len(to_predict_list)==4):
            result = ValuePredictor(to_predict_list,4)
        elif(len(to_predict_list)==8):
            result = ValuePredictor(to_predict_list,8)
        elif(len(to_predict_list)==7):
            result = ValuePredictor(to_predict_list,7)
    
    if(int(result)==1):
        prediction = "Sorry you have high chances of getting the disease. Please consult the doctor immediately"
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease."
    return(render_template("result.html", prediction_text=prediction))       





if __name__ == "__main__":
    app.run(debug=True)