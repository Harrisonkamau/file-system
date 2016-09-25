from flask import Flask, redirect, render_template,request, url_for, g, flash
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user


# import local modules
import forms
import models


# create an instance of Flask
app = Flask(__name__)

# create a login manager
login_manager = LoginManager()
# set up the login manager for the app
login_manager.init_app(app)
login_manager.login_view = 'login'


# load user route
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:  # exception got from peewee
        return None


# create a before request route
@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


# create an after request route
@app.after_request
def after_request(response):
    """Close the database after each request"""
    g.db.close()
    return response


# create a register route to register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Registration successful!', 'success')
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# create a login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your emails and password do not match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Successfully logged in!!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your emails and password do not match!", "error")
    return render_template('login.html', form=form)


# create a logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for('index'))

# create a home route
@app.route('/')
def index():
    return "This is home"


# create a secret key
app.secret_key = 'rbian.yarrh.iongdp.rojtce.gethrea'


# start the server
if __name__== "__main__":
    models.initialize()
    try:
        models.User.create_user(
            username='harrisonkamau',
            email='kamauharry@yahoo.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass