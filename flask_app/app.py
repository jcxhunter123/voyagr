from flask import Flask, render_template, request, redirect, url_for
from forms import SearchForm, QuestionnaireSlider, QuestionnaireButton
import requests
import json
from flask_bootstrap import Bootstrap
from pathlib import Path
from os import listdir
from os.path import isfile, join
import re
import ast


app = Flask(__name__, static_folder= '/static')
app.config['SECRET_KEY'] = '3141592653589793238462643383279502884197169399'

app._static_folder = 'static'
Bootstrap(app) 

# INDEX PAGE
@app.route("/#")
@app.route("/") 
@app.route("/index")
def index():
    return render_template('index.html')

# PRODUCT PAGE ----------------------------------------------------------------------------------------------------------------
@app.route("/product", methods=['GET', 'POST']) 
def product():
    form = SearchForm(meta={'csrf': False})
    print(form.errors)
    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")
    print(form.username)
    print('-----------------------------------------')
    print(form.errors)
    if form.validate_on_submit():
        print('Successful')
        return redirect(url_for('igsearch', username=form.username.data))
    return render_template('product.html', form=form)

# After Username input, Call Flask's RESTful API to scrape pictures of profiles 
@app.route("/search/<username>")
# Scrape profiles in the background
def igsearch(username):
    user = requests.get('http://127.0.0.1:5000/search/'+username)
    #user = user.json()['username']
    return redirect(url_for('questionnaire',username= username))
    # return render_template('result.html', user=user)

# "Let's get started" for users to input
@app.route("/search/<username>/questionnaire")
def questionnaire(username):
    return render_template('questionnaire.html', user=username)
    
# Question 1 - sliders 
@app.route("/search/<username>/questionnaire/1", methods=['GET', 'POST'])
def questionnaire1(username):
    form = QuestionnaireSlider()
    if form.validate_on_submit():
        # Post form data TO server
        dictToSend = {"question1":form.answer.data}
        res = requests.post('http://127.0.0.1:5000/questionnaire/answer', json=dictToSend)
        # Read POSTED data FROM server
        dictFromServer = res.json()
        print(dictFromServer)
        return redirect(url_for('questionnaire2', username=username, form=form))
    return render_template('questionnaire1.html',form=form)

# Question 2 - buttons 
@app.route("/search/<username>/questionnaire/2", methods=['GET', 'POST'])
def questionnaire2(username):
    form = QuestionnaireButton()
    if form.validate_on_submit():
        if form.low.data:
            answer = form.low.label.text
        elif form.meh.data:
            answer = form.meh.label.text
        elif form.okay.data:
            answer = form.okay.label.text
        elif form.high.data:
            answer = form.high.label.text
        # Post form data TO server
        dictToSend = {"question2":answer}
        res = requests.post('http://127.0.0.1:5000/questionnaire/answer', json=dictToSend)
        # Read POSTED data FROM server
        dictFromServer = res.json()
        print(dictFromServer)
        return redirect(url_for('questionnaire3', username=username, form=form))
    return render_template('questionnaire2.html',form=form)

# Question 3 - buttons 
@app.route("/search/<username>/questionnaire/3", methods=['GET', 'POST'])
def questionnaire3(username):
    form = QuestionnaireButton()
    if form.validate_on_submit():
        if form.yes.data:
            answer = form.yes.label.text
        elif form.no.data:
            answer = form.no.label.text
        elif form.idk.data:
            answer = form.idk.label.text
        elif form.idc.data:
            answer = form.idc.label.text
        # Post form data TO server
        dictToSend = {"question3":answer}
        res = requests.post('http://127.0.0.1:5000/questionnaire/answer', json=dictToSend)
        # Read POSTED data FROM server
        dictFromServer = res.json()
        print(dictFromServer)
        return redirect(url_for('predict', username=username, form=form))
    return render_template('questionnaire3.html', form = form)

# Please wait page for model predictions
# @app.route("/search/<username>/pleasewait", methods=['GET', 'POST'])
# def pleasewait(username):
#     return render_template('pleasewait.html')

def extract_img_path(username):
    prefix = '/static/model_inputs/'+username+'/'
    path = './static/model_inputs/'+username
    images_name = [f for f in listdir(path) if (isfile(join(path, f)) and f[-3:]=='jpg')]
    paths = [prefix+img for img in images_name]
    return paths

@app.route("/search/<username>/predict", methods=["POST", "GET"])
def predict(username):
    paths = extract_img_path(username)
    return render_template('predict.html',images=paths,username=username)

@app.route("/predict-result", methods=["GET","POST"])
def predict_result():
    if request.method == 'POST':
        predictions,prdns = [],[]
        #print(request.form.to_dict())

        result_str = request.form.to_dict()['topic']
        
        #photos = request.form.to_dict()['inputs']
        username = request.form.to_dict()['username']
        images = extract_img_path(username)
        results = ast.literal_eval(result_str)
        for result in results:
            d = {l['label']:l['prob'] for l in result}
            predictions.append(d)
            top = max(d, key=d.get)
            top_prob = d.get(top)
            prdns.append((top,top_prob))

        COUNT = {'Food':0,'Outdoor':0,'Arts':0,'Citylife':0,'Sights':0}
        for prediction in [i for i,j in prdns]:
            if prediction in ("Art Gallery",'Artwork','Contemp_Architectural','Church','Concert'):
                COUNT['Arts'] += 1
            elif prediction in ("Food", "Drinks"):
                COUNT['Food'] += 1
            elif prediction in ("Beaches", "Bike_Tours", "Boat_hire", "Camping", "Outdoor Activites", "Parks", "Eco_tours", "Hiking", "Sailing", "Scuba_Diving", "Skiing", "Water_sports"):
                COUNT['Outdoor'] += 1
            elif prediction in ("Bars n Clubs","Restaurant","Shopping Mall", "Shop"):
                COUNT['Citylife'] += 1
            elif prediction == "Sights":
                COUNT['Sights'] += 1
    return render_template('predict-result.html',d=prdns,images=images,count=COUNT)#, top=top, top_prob=top_prob)

# END PRODUCT PAGE ------------------------------------------------------------------------------------------------------------------------------

# API PAGE
@app.route("/api")
def api():
    return render_template('api.html')

# ABOUT PAGE
@app.route("/about")
def about():
    return render_template('about.html')

# CONTACT PAGE
@app.route("/contact")
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
   app.run(debug=True, port=80)
