from flaskhrs import db, login_manager
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False)
    display_name = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    doctor = db.relationship('Doctor', backref='user', uselist=False)
    patient = db.relationship('Patient', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return f"User('{self.role}', '{self.email}', '{self.password}')"


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), default='Stephen')
    last_name = db.Column(db.String(30), default='Strange')
    patients = db.relationship('Patient', backref='patients', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.first_name}', '{self.last_name}',' {self.user_id}')"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), default='John')
    last_name = db.Column(db.String(30), default='Smith')
    gender = db.Column(db.String(10), nullable=False)
    race = db.Column(db.String(10), nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    mr = db.relationship('MedRecord', backref='patient', lazy=True, uselist=False)

    @hybrid_property
    def age(self):
        today = date.today()
        birthday = self.birthday
        return today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

    def __repr__(self):
        return f"Patient('{self.gender}', '{self.race}', '{self.birthday}', '{self.age}', '{self.doctor_id}')"


class MedRecord(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    smk = db.Column(db.Integer, default=0, nullable=False)
    marital = db.Column(db.Integer, default=0, nullable=False)
    education = db.ColumnProperty(db.Integer, default=0)
