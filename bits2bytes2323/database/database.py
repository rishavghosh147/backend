from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///bit.db'
db=SQLAlchemy(app)
migrate=Migrate(app,db)

class Event(db.Model):
    event_name=db.Column(db.String(50),primary_key=True,nullable=False)
    event_type=db.Column(db.String(50),nullable=False)
    about_event=db.Column(db.String(1000),nullable=False)
    start_date=db.Column(db.String(100),nullable=False)
    event_image=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return jsonify({'event_name':self.event_name,'envent_type':self.event_type,'about_event':self.about_event,'start_date':self.start_date,'event_image':self.event_image})
    
class Coordinetor(db.Model):
    email=db.Column(db.String(50),primary_key=True,nullable=False)
    mobile=db.Column(db.String(50),primary_key=True,nullable=False)
    fname=db.Column(db.String(1000),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    event_name=db.Column(db.String(50),nullable=False)
    status=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return jsonify({'email':self.email,'mobile':self.mobile,'fname':self.fname,'lname':self.lname,'event_name':self.event_name})
    
class Participents(db.Model):
    user=db.Column(db.String(50),primary_key=True,nullable=False)

    def __repr__(self):
        return self.user
    
class User(db.Model):
    email=db.Column(db.String(50),primary_key=True,nullable=False)
    mobile=db.Column(db.String(50),primary_key=True,nullable=False)
    roll=db.Column(db.Integer,primary_key=True,nullable=False)
    fname=db.Column(db.String(1000),nullable=False)
    lname=db.Column(db.String(100),nullable=False)
    stream=db.Column(db.String(10),nullable=False)
    year=db.Column(db.String(10),nullable=False)
    password=db.Column(db.String,nullable=False)

    def __repr__(self):
        return self.email
    
class Contact(db.Model):
    mobile=db.Column(db.Integer, primary_key=True,nullable=False)
    email=db.Column(db.String(100),nullable=True)
    name= db.Column(db.String(100),nullable=False)
    role=db.Column(db.String(200),nullable=False)
    about=db.Column(db.String(200),nullable=False)
    image=db.Column(db.String(50),nullable=False)
    type=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return self.email,self.mobile,self.name,self.role,self.about,self.image

class Crew(db.Model):
    mobile=db.Column(db.Integer,primary_key=True,nullable=False)
    name=db.Column(db.String(50),nullable=False)
    role=db.Column(db.String(50),nullable=True)
    facebook=db.Column(db.String(100),nullable=True)
    instagram=db.Column(db.String(100),nullable=True)
    linkdin=db.Column(db.String(100),nullable=True)
    github=db.Column(db.String(100),nullable=True)
    type=db.Column(db.String(50),nullable=False)

    def __repr__(self):
        return self.mobile,self.name,self.role,self.facebook,self.instagram,self.linkdin,self.github
