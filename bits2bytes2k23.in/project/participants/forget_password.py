from app import app
from flask_restful import Resource
from flask import json,request,jsonify,make_response
from authentication.send_otp import send_otp
from werkzeug.security import generate_password_hash
from database.database import User,db,Temp_otp
import random,jwt
from key.keys import otp_virify_secret_key

class forget_password(Resource): #done
    def post(self):
        data=json.loads(request.data)
        if 'email' in data:
            user=User.query.filter_by(email=data['email'].lower()).first()
            if user and len(data)==2 and data['email'] and data['password']:
                otp=random.randint(100000,999999)
                check=Temp_otp.query.filter_by(login_email=data['email'].lower()).first()
                if check:
                    db.session.delete(check)
                us=Temp_otp(login_email=data['email'].lower(),otp=otp,password=generate_password_hash(data['password']))
                db.session.add(us)
                db.session.commit()
                return self.common(user.fname,otp,user.email)
        elif 'roll' in data:
            user=User.query.filter_by(roll=int(data['roll'])).first()
            if user and len(data)==2 and data['roll'] and data['password']:
                otp=random.randint(100000,999999)
                check=Temp_otp.query.filter_by(login_email=user.email).first()
                if check:
                    db.session.delete(check)
                us=Temp_otp(login_email=user.email,otp=otp,password=generate_password_hash(data['password']))
                db.session.add(us)
                db.session.commit()
                return self.common(user.fname,otp,user.email)
        return jsonify({"error":"user does not exist"})
    
    def common(self,fname,otp,email):
        msg=f"hi,{fname} this {otp} is for forget password"
        send_otp('forget password',email,msg)
        payload={"email":email,"forget":True}
        token=jwt.encode(payload,otp_virify_secret_key,algorithm='HS256')
        return jsonify({"successful":"please enter the otp","verification":token.decode('utf-8')})