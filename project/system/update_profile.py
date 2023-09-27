from flask_restful import Resource
from flask import request
from key.keys import admin_secret_key,participants_secret_key
from database.database import db,User
from authentication.token_validation import token_validation_common,user_email
from system.data_validity import UpdateProfile
from for_all.response import resp
from marshmallow import ValidationError

class update_profile(Resource): #done
    @token_validation_common
    def post(self,type):
        marshmallow=UpdateProfile()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        
        if type=="participant":
            email=user_email(participants_secret_key)
            user=User.query.filter_by(email=email).first()
            test=validate(user,data['mobile'])
            if test is not None: return test
            user.fname=data['fname']
            user.lname=data['lname']
            user.mobile=data['mobile']
            user.stream=data['stream']
            user.year=data['year']
        elif type=="admin":
            email=user_email(admin_secret_key)
            user=User.query.filter_by(email=email).first()
            test=validate(user,data['mobile'])
            if test is not None: return test
            user.fname=data['fname']
            user.lname=data['lname']
            user.mobile=data['mobile']

        db.session.commit()
        return resp({"successful":"profile updated successfully"},200)

def validate(user,mobile):
    check=User.query.filter_by(mobile=mobile).first()
    if user.mobile!=mobile and check is not None:
        return resp({"error":f"mobile no {mobile} is registered with another user"},409)