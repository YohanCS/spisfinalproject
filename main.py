from flask import Flask, render_template, request

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from oneMenu import oneMeal
import os


DININGHALL = os.path.join('static', 'Dininghalls') #for the one image - got help from https://stackoverflow.com/questions/46785507/python-flask-display-image-on-a-html-page

                          
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = DININGHALL

columns = ["Food Item", "Price", "Serving", "Calories Per Serving", "Calories Per Dollar", "Protein Per Serving"]

@app.route('/')
def render_home():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')
    return render_template('/home/home.html',Dininghalls=Dininghalls)

# 64 Degrees
@app.route('/home_64_Degrees')
def render_home_64():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_64_Degrees.html',Dininghalls=Dininghalls)

@app.route('/result_64')
def render_result_64():
    try:
        x = oneMeal(request.args["meal"], "64Degrees")
        return render_template('/result/result_64.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')



@app.route('/home_cafeV')
def render_home_cafeV():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_cafeV.html',Dininghalls=Dininghalls)

@app.route('/result_cafeV')
def render_result_cafeV():
    try:
        x = oneMeal(request.args["meal"], "cafeV")
        return render_template('/result/result_cafeV.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

# Canyon Vista
@app.route('/home_canyonV')
def render_home_canyonV():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_canyonV.html',Dininghalls=Dininghalls)

@app.route('/result_canyonV')
def render_result_canyonV():
    try:
        x = oneMeal(request.args["meal"], "canyonV")
        return render_template('/result/result_canyonV.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

# Foodworx
@app.route('/home_Foodworx')
def render_home_Foodworx():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_Foodworx.html',Dininghalls=Dininghalls)

@app.route('/result_Foodworx')
def render_result_Foodworx():
    try:
        x = oneMeal(request.args["meal"], "Foodworx")
        return render_template('/result/result_Foodworx.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')



@app.route('/home_OVT')
def render_home_64():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_64_Degrees.html',Dininghalls=Dininghalls)

@app.route('/result_OVT')
def render_result_OVT():
    try:
        meal = request.args["meal"]
        x = ""
        if meal == "Breakfast":
            x = pd.read_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTBreakfast.csv", names=columns)
        elif meal == "Lunch":
            x = pd.read_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTLunch.csv", names=columns)
        elif meal == "Dinner":
            x = pd.read_csv("/Users/christianjohnventura/Desktop/spis18/github/spisfinalproject2/menus/OVT/OVTDinner.csv", names=columns)
        return render_template('/result/result_OVT.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')


@app.route('/home_Pines')
def render_home_Pines():
    Dininghalls = os.path.join(app.config['UPLOAD_FOLDER'], 'Dininghalls.png')

    return render_template('/home/home_Pines.html',Dininghalls=Dininghalls)

@app.route('/result_Pines')
def render_result_Pines():
    try:
        x = oneMeal(request.args["meal"], "Pines")
        return render_template('/result/result_Pines.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

if __name__=="__main__":
    app.run(debug=False, port=54400)
