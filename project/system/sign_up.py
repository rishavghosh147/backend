from flask import request
from database.database import Temp_user,db,User
from sqlalchemy import or_
import random
from werkzeug.security import generate_password_hash
from authentication.send_otp import send_otp
from flask_restful import Resource
import jwt
from key.keys import otp_virify_secret_key,secret_key,otp_token_key
from system.data_validity import SignUp
from for_all.response import resp
from marshmallow import ValidationError

class user_signup(Resource): #done 
    
    def post(self):
        marshmallow=SignUp()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        if 'roll' in data:
            role=2
        elif 'secret_key' in data:
                if int(data['secret_key'])==secret_key:
                    role=0
                else:
                    return resp({'error':'please contact rishav ghosh for secret key'},401)

        if 'roll' in data:
            roll=data['roll']
        else:
            roll=-0
        result=check_user(data['email'],data['mobile'],roll)
         
        if result:
            return resp({"error": "this user is already exist !!!"},409)

        temp(data,role)
        payload={"email":data['email'],"type":"signup"}
        token=otp_token(payload)
        response=resp({'successful':'please enter the otp'},200)
        response.headers[otp_token_key]=token
        return response

def temp(data,role):
    otp=random.randint(100000,999999)
    hash_password=generate_password_hash(data['password'])

    if 'roll' in data:
        roll=data['roll']
    else:
        roll=121
    user=Temp_user.query.filter(or_(Temp_user.email==data['email'].lower(),Temp_user.mobile==data['mobile'],Temp_user.roll==roll)).all()
    for x in user:
        db.session.delete(x)
        db.session.commit()
        
    if role==0:
        user=Temp_user(fname=data['fname'].lower(),lname=data['lname'].lower(),email=data['email'].lower(),mobile=data['mobile'],password=hash_password,role_id=role,otp=otp)
    if role==2:
        user=Temp_user(fname=data['fname'].lower(),lname=data['lname'].lower(),email=data['email'].lower(),mobile=data['mobile'],roll=roll,password=hash_password,role_id=role,year=data['year'],stream=data['stream'].lower(),otp=otp)

    msg=f"hello, {data['fname']} this otp {otp} is for sign up verification. Please don't share it with anyone and also don't share your password."
    send_otp('for sign_up verification',data['email'].lower(),msg)
    db.session.add(user)
    db.session.commit()

def otp_token(payload):
    return jwt.encode(payload,otp_virify_secret_key,algorithm='HS256')

def check_user(email,mobile,roll):
    user=User.query.filter(or_(User.email==email,User.mobile==mobile,User.roll==roll)).all()
    temp=len(user)!=0
    return temp