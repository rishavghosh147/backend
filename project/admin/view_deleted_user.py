from database.database import Deleted_users
from flask_restful import Resource
from for_all.response import resp
from authentication.token_validation import token_validation_admin
from admin.data_validity import view_deleted_user
from marshmallow import ValidationError

class veiw_deleted_user(Resource): #checked
    @token_validation_admin
    def post(self):
        data=Deleted_users.query.all()
        users=[]
        for x in data:
            users.append({
                "fname":x.fname,
                "lname":x.lname,
                "email":x.email,
                "mobile":x.mobile,
                "roll":x.roll,
                "year":x.year,
                "stream":x.stream,
                "deleted_by":x.deleted_by
                })
        marshmallow=view_deleted_user(many=True)
        try:
            data=marshmallow.dumps(users)
        except ValidationError as e:
            return f'{e}'
        return resp(data,200)