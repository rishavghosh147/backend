from flask_restful import Resource
from flask import request
from database.database import Temp_user, User,db,Temp_otp
import jwt
from datetime import datetime, timedelta
from key.keys import otp_virify_secret_key,admin_secret_key,participants_secret_key,authorization_token_key
from system.data_validity import Otp
from for_all.response import resp
from marshmallow import ValidationError

class otp_verify(Resource): #done
    def post(self):
        if 'verification' in request.headers:
            header=request.headers.get('verification')
            marshmallow=Otp()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        try:
            verify_type=jwt.decode(header,otp_virify_secret_key,algorithms=['HS256'])
        except:
            return resp({"error":"you are not permited"},401)
        if 'signup' == verify_type['type']:
            user=Temp_user.query.filter_by(email=verify_type['email']).first()
            if user and user.otp==int(data['otp']):
                users=User(fname=user.fname,lname=user.lname,email=user.email,mobile=user.mobile,roll=user.roll,password=user.password,role_id=user.role_id,year=user.year,stream=user.stream)
                db.session.add(users)
                db.session.delete(user)
                db.session.commit()
                return resp({"successful":"user registered successfully "},200)
        elif 'login' == verify_type['type']:
            otp=Temp_otp.query.filter_by(login_email=verify_type['email']).first()
            if otp and otp.otp==int(data['otp']):
                if verify_type['role']=="0":
                    secret_key=admin_secret_key
                else:
                    secret_key=participants_secret_key

                db.session.delete(otp)
                db.session.commit()
                response=resp({"successful":"you are loged in successfully"},200)
                response.headers[authorization_token_key]=token_gen(verify_type['email'].lower(),secret_key)
                return response
        elif 'forget'  == verify_type['type']:
            otp=Temp_otp.query.filter_by(login_email=verify_type['email'].lower()).first()
            if  otp and otp.otp==int(data['otp']):
                user=User.query.filter_by(email=verify_type['email'].lower()).first()
                user.password=otp.password
                db.session.delete(otp)
                db.session.commit()
                return resp({"successful":"the password has been changed successfully"},200)
        return resp({"error":"you entered a wrong otp !!!"},403)
    
def token_gen(email,secret_key):
    time=datetime.now()+timedelta(minutes=60)
    exp_time=int(time.timestamp())
    payload={"email":email,"expire":exp_time}
    token=jwt.encode(payload,secret_key,algorithm='HS256')
    return token #.decode('utf-8')
