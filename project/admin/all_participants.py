from flask_restful import Resource
from authentication.token_validation import token_validation_admin
from database.database import User
from for_all.response import resp
from admin.data_validity import all_participants
from marshmallow import ValidationError

class users(Resource): #checked
    @token_validation_admin
    def post(self):
        user=User.query.filter(User.roll.isnot(None)).all()
        all=[]
        for x in user:
            all.append({
                "fname":x.fname,
                "lname":x.lname,
                "email":x.email,
                "mobile":x.mobile,
                "roll":x.roll,
                "stream":x.stream,
                "year":x.year})
        marshmallow=all_participants(many=True)
        try:
            data=marshmallow.dumps(all)
        except ValidationError as e:
            return f'{e}'
        return resp(data,200)