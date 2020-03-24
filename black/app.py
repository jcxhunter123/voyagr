from flask import Flask, render_template, request, redirect, url_for
import requests
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_folder= '/static')

app._static_folder = 'static'
Bootstrap(app) 

# Home page with User's Instagram Input
@app.route("/", methods=['GET', 'POST']) 
def home():
    return render_template('index.html')

@app.route("/product", methods=['GET', 'POST']) 
def singlepage():
    return render_template('product.html')

if __name__ == '__main__':
   app.run(debug=True, port=90)

