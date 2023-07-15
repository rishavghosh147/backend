from app import app
from flask_restful import Resource
from flask import request,jsonify
from key.keys import authorization_token_key,admin_secret_key,participants_secret_key
import jwt
from authentication.token_validation import token_validation_common

class User_type(Resource):
    @token_validation_common
    def post(self,type):
        return jsonify({"user":type})