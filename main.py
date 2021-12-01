from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField,PasswordField,validators
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os


app=Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("53t98ty935hg92358929gh")
Bootstrap(app)

##CREATING DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("postgres://eltoscettmvxyw:9700fd81b2b43ae6fd3a66f059916a8c48514982fe0863c2c36814e26b87806f@ec2-3-221-24-14.compute-1.amazonaws.com:5432/dfsq1krvmg2236",'sqlite:///cards.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    username = db.Column(db.String(1000))
db.create_all()


##creating table
class Cards(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(200), nullable=False)
    title=db.Column(db.String(200), nullable=False)
    img_url=db.Column(db.String, nullable=False)
    specs=db.Column(db.String, nullable=False)
    price=db.Column(db.Integer,nullable=False)
    offer=db.Column(db.Integer,nullable=False)
#db.create_all()



class Login(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField(label="Log In")

class Signup(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
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
    type = StringField(label='Classify Product', validators=[DataRequired()])
    title=StringField(label='Title', validators=[DataRequired()])
    img_url=StringField(label='Img_url', validators=[DataRequired()])
    specs=StringField(label='Specifications', validators=[DataRequired()])
    price=StringField(label='Price', validators=[DataRequired()])
    offer=StringField(label='Best Offer', validators=[DataRequired()])
    submit = SubmitField(label="Add Product")

@app.route("/",methods=["GET", "POST"])
def login():
    login_form = Login()
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        #Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        #Email exists and password correct
        else:
            login_user(user)
            if login_form.validate_on_submit():
                return redirect(url_for('home'))
    return render_template("login.html", form=login_form)

@app.route("/signup",methods=["GET", "POST"])
def signup():
    signup_form= Signup()
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get('email')).first():
            #User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        new_user = User(
            email=request.form.get('email'),
            username=request.form.get('username'),
            password=generate_password_hash(request.form.get('password'),method='pbkdf2:sha256', salt_length=8)
        )
        if signup_form.validate_on_submit():
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user)

            return render_template("home.html")
    return render_template("signup.html", form=signup_form)


@app.route("/reset",methods=["GET", "POST"])
def reset():
    form = Reset()
    if form.validate_on_submit():
        return render_template("signup.html")

    return render_template("reset.html",form=form)

@app.route("/add_card",methods=["GET", "POST"])
def add_card():
    form = Products()
    if form.validate_on_submit():
        new_card = Cards(
            type=form.type.data.lower(),
            title=form.title.data,
            img_url=form.img_url.data,
            specs=form.specs.data,
            price=int(form.price.data),
            offer=int(form.offer.data)
        )
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_card.html",form=form)


@app.route("/home")
@login_required
def home():
    cards = Cards.query.all()
    return render_template("home.html",username=current_user.username , cards=cards)

@app.route("/mobiles")
@login_required
def mobiles():
    cards=Cards.query.filter_by(type="mobiles")
    return render_template("mobiles.html", cards=cards)

@app.route("/electronics")
@login_required
def electronics():
    cards = Cards.query.filter_by(type="electronics")
    return render_template("electronics.html", cards=cards)

@app.route("/space_store")
@login_required
def space_store():
    cards = Cards.query.filter_by(type="space store")
    return render_template("space_store.html", cards=cards)

@app.route("/makeup")
@login_required
def makeup():
    cards = Cards.query.filter_by(type="beauty and makeup")
    return render_template("makeup.html", cards=cards)

@app.route("/kitchen")
@login_required
def kitchen():
    cards = Cards.query.filter_by(type="home and kitchen")
    return render_template("kitchen.html", cards=cards)

@app.route("/computer")
@login_required
def computer():
    cards = Cards.query.filter_by(type="computer")
    return render_template("computer.html", cards=cards)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

