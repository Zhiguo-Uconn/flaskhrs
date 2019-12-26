from flask import render_template, url_for, flash, redirect, request
from flaskhrs.forms import RegistrationForm, LoginForm
from flaskhrs.models import User, Doctor, Patient
from flaskhrs import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


clients = [
    {
        'doc': 'Wang',
        'gender': 'male',
        'race': 'Asian',
        'bday': '09/28/1975',
    },
    {
        'doc': 'Stephen',
        'gender': 'male',
        'race': 'White',
        'bday': '11/28/1963',
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(role=form.role.data, display_name=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
