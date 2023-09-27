from flask_restful import Resource
from flask import request
from authentication.send_otp import send_otp
from werkzeug.security import generate_password_hash
from database.database import User,db,Temp_otp
import random,jwt
from key.keys import otp_virify_secret_key,otp_token_key
from for_all.response import resp
from system.data_validity import ForgetPassword
from marshmallow import ValidationError

class forget_password(Resource): #done
    def post(self):
        marshmallow=ForgetPassword()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'

        if 'email' in data:
            user=User.query.filter_by(email=data['email'].lower()).first()
            if user:
                otp=random.randint(100000,999999)
                check=Temp_otp.query.filter_by(login_email=data['email'].lower()).first()
                if check:
                    db.session.delete(check)
                us=Temp_otp(login_email=data['email'].lower(),otp=otp,password=generate_password_hash(data['password']))
                db.session.add(us)
                db.session.commit()
                return common(user.fname,otp,user.email)
        elif 'roll' in data:
            user=User.query.filter_by(roll=data['roll']).first()
            if user:
                otp=random.randint(100000,999999)
                check=Temp_otp.query.filter_by(login_email=user.email).first()
                if check:
                    db.session.delete(check)
                us=Temp_otp(login_email=user.email,otp=otp,password=generate_password_hash(data['password']))
                db.session.add(us)
                db.session.commit()
                return common(user.fname,otp,user.email)
        return resp({"error":"user does not exist"},404)
    
def common(fname,otp,email):
    msg=f"hi,{fname} this {otp} is for forget password"
    send_otp('forget password',email,msg)
    payload={"email":email,"type":"forget"}
    token=jwt.encode(payload,otp_virify_secret_key,algorithm='HS256')
    response=resp({"successful":"please enter the otp"},200)
    response.headers[otp_token_key]=token
    return response