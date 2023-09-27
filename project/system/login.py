from flask import request
from werkzeug.security import check_password_hash
from database.database import User,db,Temp_otp
import jwt,random
from flask_restful import Resource
from authentication.send_otp import send_otp
from key.keys import otp_virify_secret_key,otp_token_key
from system.data_validity import ForgetPassword
from for_all.response import resp
from marshmallow import ValidationError

class User_login(Resource): #done 
    def post(self):
        marshmallow=ForgetPassword()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        otp=random.randint(100000,999999)

        if 'roll' in data:
            check=User.query.filter_by(roll=data['roll']).first()
            if check and check_password_hash(check.password,data['password']):
                email=check.email
                role=check.role_id
            elif check and not check_password_hash(check.password,data['password']):
                return resp({"error":"you entered a wrong password"},401)
            else:
                return resp({"error":"user does not exist"},404)
        else:
            check=User.query.filter_by(email=data['email']).first()
            if check and check_password_hash(check.password,data['password']):
                email=data['email'].lower()
                role=check.role_id
            elif check and not check_password_hash(check.password,data['password']):
                return resp({"error":"you entered a wrong password"},401)
            else:
                return resp({"error":"user does not exist"},404)
            
        previous=Temp_otp.query.filter_by(login_email=email).first()
        if previous:
            db.session.delete(previous)
        db.session.commit()
        msg=f"this {otp} is for login veification. please don't share with any one"
        send_otp('login verification',email,msg)
        save_otp=Temp_otp(login_email=email,otp=otp)
        db.session.add(save_otp)
        db.session.commit()
        response=resp({"successful":"please enter the otp"},200)
        response.headers[otp_token_key]=login_token(email,role)
        return response
    
def login_token(email,role):
    payload={"email":email,"role":f'{role}',"type":"login"}
    encode=jwt.encode(payload,otp_virify_secret_key,algorithm='HS256')
    return encode #.decode('utf-8')
