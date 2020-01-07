from flask import render_template, url_for, flash, redirect, request, session
from flaskhrs.forms import RegistrationForm, LoginForm, PatientForm
from flaskhrs.models import User, Doctor, Patient
from flaskhrs import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', user=current_user)


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
        if form.role.data == 'D':
            doc = Doctor(first_name='', last_name='', user_id=user.id)
            db.session.add(doc)
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


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='HRS Dashboard')


@app.route("/newpatient", methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          gender=form.gender.data,
                          race=form.race.data,
                          birthday=form.birthday.data,
                          doctor_id=current_user.id)
        db.session.add(patient)
        db.session.commit()
        flash('New patient has been created!', 'success')
        print(f'patient is {patient}')

        return redirect(url_for('home'))
    return render_template('newpatient.html', title='Create New Patient', form=form, topic='New Patient')


@app.route('/sessions')
def sessions():
    pass

