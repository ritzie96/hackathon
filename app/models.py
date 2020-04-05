from app import db
from app import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'crisis_user'
    __table_args__ = { 'extend_existing': True }
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)    
    password = db.Column(db.String(150))
    municipality = db.Column(db.String(150))
    city = db.Column(db.String(150))
    country= db.Column(db.String(150), default = 'sweden')
    roles = db.Column(db.String, default='user')

    def __repr__(self):
        return '<User {}>'.format(self.username)    


class Employee(db.Model):
    __tablename__ = 'crisis_employee'
    __table_args__ = { 'extend_existing': True }
   
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150))
    name = db.Column(db.String(150))
    birth_date = db.Column(db.String(150))
    phone_no = db.Column(db.String)
    add_email_id = db.Column(db.String(150))
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)
    city = db.Column(db.String(150))
    municipality = db.Column(db.String(150))
    country = db.Column(db.String(150))
    year = db.Column(db.String(10))
    time = db.Column(db.String(150))
    address = db.Column(db.String(150))
    skills = db.Column(db.String)
    role = db.Column(db.String(150))
