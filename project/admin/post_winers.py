from database.database import Winers,db
from flask_restful import Resource
from authentication.token_validation import token_validation_admin
from flask import request
from admin.data_validity import PostWiners
from marshmallow import ValidationError
from for_all.response import resp

class winers(Resource): #!!!
    @token_validation_admin
    def post(self):
        marshmallow=PostWiners()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return resp({'error':e},406)
        if 'roll' in data:
            ch=Winers.query.filter(Winers.roll==data['roll'],Winers.event_name==data['event_name'])
            if ch:
                return resp({"error":"already exist"},409)
            user=Winers(roll=data['roll'],event_name=data['event_name'],marks=data['marks'])
            db.session.add(user)
            db.session.commit()
            return resp({"successful":"successfully added"},200)
        else:
            ch=Winers.query.filter(Winers.team_name==data['team_name'],Winers.event_name==data['event_name'])
            if ch:
                return resp({"error":"already exist"},409)
            check=Winers(team_name=data['team_name'],event_name=data['event_name'],marks=data['marks'])
            db.session.add(check)
            db.session.commit()
            return resp({"successful":"successfully added"},200)

