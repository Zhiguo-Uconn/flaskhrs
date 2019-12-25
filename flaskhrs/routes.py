from flask import render_template, url_for, flash, redirect
from flaskhrs.forms import RegistrationForm, LoginForm
from flaskhrs.models import User, Doctor, Patient
from flaskhrs import app


clients = [
    {
        'doc': 'Stephen',
        'gender': 'male',
        'race': 'Asian',
        'bday': '09/28/1975',
    },
    {
        'doc': 'Stephen',
        'gender': 'male',
        'race': 'Asian',
        'bday': '09/28/1973',
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', clients=clients)


@app.route('/about')
def about():
    return 'About'


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

