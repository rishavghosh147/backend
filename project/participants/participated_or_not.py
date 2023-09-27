from database.database import Participants,Team_data,db,Event,User,Team_participate
from flask_restful import Resource
from flask import request
from key.keys import participants_secret_key
from authentication.token_validation import token_validation_participents,user_email
from for_all.response import resp
from participants.data_validity import EventName
from marshmallow import ValidationError

class praricipated_or_not(Resource): #!!!
    @token_validation_participents
    def post(self):
        marshmallow=EventName()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        email=user_email(participants_secret_key)
        roll=User.query.filter_by(email=email).first()
        event=Event.query.filter_by(event_name=data['event_name']).first()
        if event.team==1:
            user=db.session.query(Team_data).join(Team_participate,Team_participate.event_name==data['event_name']).filter(Team_data.roll==roll.roll).first()
            if user is not None:
                return resp({"successful":1},200)
            else:
                return resp({"successful":0},404)
        else:
            user=Participants.query.filter(Participants.roll==roll.roll,Participants.event_name==data['event_name']).first()
            if user:
                return resp({"successful":1},200)
            else:
                return resp({"successful":0},404)