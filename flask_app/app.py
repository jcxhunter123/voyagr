from flask import Flask, render_template, request, redirect, url_for
from forms import SearchForm, QuestionnaireSlider, QuestionnaireButton
import requests
import json
from flask_bootstrap import Bootstrap

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
    user = user.json()['username']
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
        return redirect(url_for('pleasewait', username=username, form=form))
    return render_template('questionnaire3.html', form = form)

# Please wait page for model predictions
@app.route("/search/<username>/pleasewait", methods=['GET', 'POST'])
def pleasewait(username):
    return render_template('pleasewait.html')

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
