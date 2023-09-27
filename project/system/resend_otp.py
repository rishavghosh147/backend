from flask import request
from flask_restful import Resource
import jwt
from key.keys import otp_virify_secret_key
from database.database import Temp_otp,Temp_user,db
import random
from authentication.send_otp import send_otp
from key.keys import otp_virify_secret_key
from for_all.response import resp

class resend_otp(Resource): #done
    def post(self):
        temp=request.headers.get('verification')
        try:
            header=jwt.decode(temp,otp_virify_secret_key,algorithms=['HS256'])
        except ValueError as e:
            return resp({"error":f"{e}"},200)
        otp=random.randint(100000,999999)
        if 'login' == header['type']:
            user=Temp_otp.query.filter_by(login_email=header['email']).first()
            user.otp=otp
            db.session.commit()
            msg=f"this {otp} is for login veification. please don't share with any one"
            send_otp('login verification',header['email'],msg)
            return resp({"successful":"otp has been resend"},200)
        elif 'signup' == header['type']:
            user=Temp_user.query.filter_by(email=header['email']).first()
            user.otp=otp
            db.session.commit()
            msg=f"this {otp} is for sign up veification. please don't share with any one"
            send_otp('sign up verification',header['email'],msg)
            return resp({"successful":"otp has been resend"},200)
        elif 'forget' == header['type']:
            user=Temp_otp.query.filter_by(login_email=header['email']).first()
            user.otp=otp
            db.session.commit()
            msg=f"this {otp} is for forget password. please don't share with any one"
            send_otp('forget password verification',header['email'],msg)
            return resp({"successful":"otp has been resend"},200)
        else:
            return resp({"error":"invalid request !!!"},401)