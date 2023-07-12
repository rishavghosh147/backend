from app import app
from flask_restful import Resource
from authentication.token_validation import token_validation_admin
from database.database import User
from flask import jsonify

class users(Resource):
    @token_validation_admin
    def post(self):
        user=User.query.filter(User.roll.isnot(None)).all()
        all=[]
        for x in user:
            all.append(
                {
                    "fname":x.fname,
                    "lname":x.lname,
                    "email":x.email,
                    "mobile":x.mobile,
                    "roll":x.roll,
                    "stream":x.stream,
                    "year":x.year
                }
            )
        return jsonify(all)