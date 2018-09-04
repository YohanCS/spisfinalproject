from flask import Flask, render_template, request

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from oneMenu import oneMeal

app = Flask(__name__)


@app.route('/')
def render_home():
    return render_template('/home/home.html')

# 64 Degrees
@app.route('/home_64_Degrees')
def render_home_64():
    return render_template('/home/home_64_Degrees.html')

@app.route('/result_64')
def render_result_64():
    try:
        x = oneMeal(request.args["meal"], "64Degrees")
        return render_template('/result/result_64.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

# Cafe Ventanas
@app.route('/home_cafeV')
def render_home_cafeV():
    return render_template('/home/home_cafeV.html')

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
    return render_template('/home/home_canyonV.html')

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
    return render_template('/home/home_Foodworx.html')

@app.route('/result_Foodworx')
def render_result_Foodworx():
    try:
        x = oneMeal(request.args["meal"], "Foodworx")
        return render_template('/result/result_Foodworx.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

# OceanView Terrace
@app.route('/home_OVT')
def render_home_OVT():
    return render_template('/home/home_OVT.html')

@app.route('/result_OVT')
def render_result_OVT():
    try:
        x = oneMeal(request.args["meal"], "OVT")
        return render_template('/result/result_OVT.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

# Pines
@app.route('/home_Pines')
def render_home_Pines():
    return render_template('/home/home_Pines.html')

@app.route('/result_Pines')
def render_result_Pines():
    try:
        x = oneMeal(request.args["meal"], "Pines")
        return render_template('/result/result_Pines.html', data=x.to_html(classes="mystyle", justify="center"))
    except:
        return render_template('error.html')

if __name__=="__main__":
    app.run(debug=False, port=54400)
