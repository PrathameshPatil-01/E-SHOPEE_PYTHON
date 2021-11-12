from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,PasswordField,validators
from wtforms.validators import DataRequired, Email, Length



app=Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


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

@app.route("/mobiles")
def mobiles():
    return render_template("mobiles.html")

@app.route("/home")
def home():
    return render_template("home.html")





if __name__ == '__main__':
    app.run(debug=True)

