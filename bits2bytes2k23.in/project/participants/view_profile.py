from app import app
from flask_restful import Resource
from flask import request,jsonify
import jwt
from database.database import User
from key.keys import participants_secret_key,admin_secret_key
from authentication.token_validation import token_validation_common,user_email

class veiw_profile(Resource): #done
    @token_validation_common
    def post(self,type):
        if type=="participant":
            email=user_email(participants_secret_key)
            user=User.query.filter_by(email=email).first()
            return jsonify({"fname":user.fname,"lname":user.lname,"email":user.email,"mobile":user.mobile,"roll":user.roll,"year":user.year,"stream":user.stream})
        elif type=="admin":
            email=user_email(admin_secret_key)
            user=User.query.filter_by(email=email).first()
            return jsonify({"fname":user.fname,"lname":user.lname,"email":email,"mobile":user.mobile})
        else:
            return jsonify({"error":"something went wrong !!!"})
