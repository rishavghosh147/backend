from flask_restful import Resource
from authentication.token_validation import token_validation_common
from for_all.response import resp

class User_type(Resource): #done
    @token_validation_common
    def post(self,type):
        return resp({"user":type},200)