from app import app
from flask import json,request, make_response, jsonify
from werkzeug.security import generate_password_hash,check_password_hash
from database.database import User,db,Temp_otp
from datetime import datetime, timedelta
import jwt,random
from flask_restful import Resource
from authentication.send_otp import send_otp
from key.keys import otp_virify_secret_key
from authentication.return_respose import response

class User_login(Resource): #done 
    def post(self):
        data=json.loads(request.data)
        otp=random.randint(100000,999999)

        previous=Temp_otp.query.filter_by(login_email=data['email']).first()
        if previous:
            db.session.delete(previous)

        if 'roll' in data:
            check=User.query.filter_by(roll=data['roll']).first()
            if check and check_password_hash(check.password,data['password']):
                email=check.email
                role=check.role_id
            elif check and not check_password_hash(check.password,data['password']):
                return response(jsonify({"error":"you entered a wrong password"}),401)
            else:
                return response(jsonify({"error":"user does not exist"}),204)
        else:
            check=User.query.filter_by(email=data['email'].lower()).first()
            if check and check_password_hash(check.password,data['password']):
                email=data['email']
                role=check.role_id
            elif check and not check_password_hash(check.password,data['password']):
                return response(jsonify({"error":"you entered a wrong password"}),401)
            else:
                return response(jsonify({"error":"user does not exist"}),204)
            
            msg="this {otp} is for login veification. please don't share with any one"
            send_otp('login verification',email,msg)
            save_otp=Temp_otp(login_email=email,otp=otp)
            db.session.add(save_otp)
            db.session.commit()
            message={"successful":"please enter the otp"}
            resp=make_response(jsonify(message))
            resp.headers.set('veification',f'{self.login_token(email,role)}')
            return response(resp,200)
    
    def login_token(self,email,role):
        payload={"email":f'{email}',"role":f'{role}',"login":True}
        encode=jwt.encode(payload,otp_virify_secret_key,algorithm='HS256')
        return encode
