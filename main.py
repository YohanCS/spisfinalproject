from flask import Flask, render_template, request

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from oneMenu import oneMeal

app = Flask(__name__)


@app.route('/')
def render_home():
    return render_template('home.html')

@app.route('/result')
def render_result():
    try:
        x = oneMeal(request.args["meal"])
        return render_template('result.html', data=x.to_html())
    except:
        return render_template('error.html')
  
    
#running it and using the port
if __name__=="__main__":
    app.run(debug=False, port=54400)
