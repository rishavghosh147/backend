from app import app
from flask import json,request,jsonify
from database.database import User,db,Deleted_users
from authentication.token_validation import token_validation_admin,user_email
from flask_restful import Resource
import jwt
from key.keys import admin_secret_key

class delete_user(Resource): #done
    @token_validation_admin
    def post(self):
        data=json.loads(request.data)
        user=User.query.filter_by(roll=int(data['roll'])).first()
        if user:
            email=user_email(admin_secret_key)
            temp_user=Deleted_users(fname=user.fname,lname=user.lname,email=user.email,mobile=user.mobile,roll=user.roll,year=user.year,stream=user.stream,deleted_by=email)
            db.session.add(temp_user)
            db.session.delete(user)
            db.session.commit()
            return jsonify({'successful':'user deleted successfully'})
        else:
            return jsonify({'error':'user does not exist'})