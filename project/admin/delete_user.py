from flask import request
from database.database import User,db,Deleted_users
from authentication.token_validation import token_validation_admin,user_email
from flask_restful import Resource
from key.keys import admin_secret_key
from admin.data_validity import DeleteUser
from for_all.response import resp
from marshmallow import ValidationError

class delete_user(Resource): #checked
    @token_validation_admin
    def post(self):
        marshmallow=DeleteUser()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        user=User.query.filter_by(roll=data['roll']).first()
        if user:
            email=user_email(admin_secret_key)
            temp_user=Deleted_users(fname=user.fname,lname=user.lname,email=user.email,mobile=user.mobile,roll=user.roll,year=user.year,stream=user.stream,deleted_by=email)
            db.session.add(temp_user)
            db.session.delete(user)
            db.session.commit()
            return resp({'successful':'user deleted successfully'},200)
        else:
            return resp({'error':'user does not exist'},404)