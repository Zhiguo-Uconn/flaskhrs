from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, BooleanField, RadioField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskhrs.models import User
from flaskhrs.support import df


class RegistrationForm(FlaskForm):
    username = StringField('Display Name', validators=[Length(min=2, max=40)], default='Strange')
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('I am a/an', choices=[('D', 'Doctor'), ('P', 'Individual')])
    first_name = StringField('First Name', default='')
    last_name = StringField('Last Name', default='')
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Display Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Length(max=20)])
    last_name = StringField('Last Name',
                            validators=[Length(max=20)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[Length(min=2, max=40)])
    last_name = StringField('Last Name', validators=[Length(min=2, max=40)])
    gender = SelectField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    race = SelectField('Race',
                       choices=[('White', 'White'), ('Black', 'Black'), ('Asian', 'Asian'), ('AI', 'American Indian'),
                                ('Hispanic', 'Hispanic')])
    birthday = DateField('Date of Birth')
    submit = SubmitField('Create New Patient')


class MedForm(FlaskForm):
    smk = SelectField('Smoking', choices=df.get_choices('smk'), default=0)
    marital = SelectField('Marital Status', choices=df.get_choices('MaritalStatus'), default=0)
    education = SelectField('Education', choices=df.get_choices('Education'), default=0)
    bmi = SelectField('BMI', choices=df.get_choices('BMI'), default=0)
    alcohol = SelectField('Alcohol Consumption', choices=df.get_choices('Alcohol'), default=0)
    physical = SelectField('Physical Activity', choices=df.get_choices('Physical Activity'), default=0)


