from flask import Flask, render_template, request

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from oneMenu import oneMeal

app = Flask(__name__)


@app.route('/')
def render_main():
    x = oneMeal('breakfast')
    return render_template('home.html', data=x.to_html())

@app.route('/result'):
    return render_template('result.html')
    
#running it and using the port
if __name__=="__main__":
    app.run(debug=False, port=54390)
