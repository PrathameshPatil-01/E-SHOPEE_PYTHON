from flask import Flask, render_template,url_for,request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,PasswordField,validators
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy



app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATING DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##creating table
class Cards(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    img_url=db.Column(db.String, nullable=False)
    specs=db.Column(db.String, nullable=False)
    price=db.Column(db.Integer,nullable=False)
    offer=db.Column(db.Integer,nullable=False)
db.create_all()



class Login(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")

class Signup(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField('Password', [
        validators. Length(min=8),
        validators.DataRequired()
    ])
    confirm = PasswordField('Confirm Password', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])

    submit = SubmitField(label="Sign Up")

class Reset(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    submit = SubmitField(label="Send Verification Code")

class Products(FlaskForm):
    title=StringField(label='Title', validators=[DataRequired()])
    img_url=StringField(label='Img_url', validators=[DataRequired()])
    specs=StringField(label='Specifications', validators=[DataRequired()])
    price=StringField(label='Price', validators=[DataRequired()])
    offer=StringField(label='Best Offer', validators=[DataRequired()])
    submit = SubmitField(label="Add Product")

@app.route("/",methods=["GET", "POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        return render_template("home.html")

    return render_template("login.html", form=login_form)

@app.route("/signup",methods=["GET", "POST"])
def signup():
    signup_form= Signup()
    if signup_form.validate_on_submit():
        return render_template("home.html")
    return render_template("signup.html", form=signup_form)


@app.route("/reset",methods=["GET", "POST"])
def reset():
    form = Reset()
    if form.validate_on_submit():
        return render_template("signup.html")

    return render_template("reset.html",form=form)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/mobiles")
def mobiles():
    return render_template("mobiles.html")

@app.route("/electronics")
def electronics():
    return render_template("electronics.html")

@app.route("/space_store")
def space_store():
    return render_template("space_store.html")

@app.route("/makeup")
def makeup():
    return render_template("makeup.html")

@app.route("/kitchen")
def kitchen():
    return render_template("kitchen.html")

@app.route("/computer")
def computer():
    return render_template("computer.html")


@app.route("/add_card",methods=["GET", "POST"])
def add_card():
    form = Products()
    if form.validate_on_submit():
        return render_template("home.html")

    return render_template("add_card.html",form=form)


if __name__ == '__main__':
    app.run(debug=True)

