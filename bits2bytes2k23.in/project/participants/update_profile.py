from app import app
from flask_restful import Resource
from flask import json,request,jsonify
from key.keys import admin_secret_key,participants_secret_key
import jwt
from database.database import db,User
from authentication.token_validation import token_validation_common,user_email

class update_profile(Resource): #done
    @token_validation_common
    def post(self,type):
        data=json.loads(request.data)
        if len(data)==5 and data['fname'] and data['lname'] and data['mobile'] and data['stream'] and data['year'] and type=="participant":
            email=user_email(participants_secret_key)
            user=User.query.filter_by(email=email).first()
            user.fname=data['fname']
            user.lname=data['lname']
            user.mobile=int(data['mobile'])
            user.stream=data['stream']
            user.year=int(data['year'])
            db.session.commit()
            return jsonify({"successful":"profile updated successfully"})
        elif len(data)==3 and data['fname'] and data['lname'] and data['mobile'] and type=="admin":
            email=user_email(admin_secret_key)
            user=User.query.filter_by(email=email).first()
            user.fname=data['fname']
            user.lname=data['lname']
            user.mobile=int(data['mobile'])
            db.session.commit()
            return jsonify({"successful":"profile updated successfully"})
        else:
            return jsonify({"error":"the data is not valid"})
