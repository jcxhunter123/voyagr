from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import IntegerRangeField
from wtforms.widgets import html_params, HTMLString

class SearchForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(), Length(min=2, max =50)])

class QuestionnaireSlider(FlaskForm):
    answer = IntegerRangeField('answer',default=5)

class QuestionnaireButton(FlaskForm):
    # Yes / No / I don't know / Doesn't Matter
    yes = SubmitField('Yes', render_kw={"class": "btn btn-primary"})
    no = SubmitField('No', render_kw={"class": "btn btn-primary"})
    idk = SubmitField("I'm not sure",render_kw={"class": "btn btn-primary"})
    idc = SubmitField("I don't care", render_kw={"class": "btn btn-primary"})

    # Low - High Range 
    low = SubmitField('Not too much', render_kw={"class": "btn btn-primary"})
    meh = SubmitField('So-So', render_kw={"class": "btn btn-primary"})
    okay = SubmitField('Relatively',render_kw={"class": "btn btn-primary"})
    high = SubmitField('Utmost', render_kw={"class": "btn btn-primary"})

