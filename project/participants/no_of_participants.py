from flask_restful import Resource
from flask import request
from database.database import Event,db,Team_participate,Participants
from participants.data_validity import EventName
from for_all.response import resp
from marshmallow import ValidationError

class no_of_participants(Resource): #checked
    def post(self):
        marshmallow=EventName()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        team=Event.query.filter_by(event_name=data['event_name']).first()
        if team.team ==1:
            count=db.session.query(Team_participate).filter_by(event_name=data['event_name']).count() #.group_by(Team_participate.team_name).count()
            return resp({"successful":count},200)
        elif team.team==0:
            count=Participants.query.filter_by(event_name=data['event_name']).count()
            return  resp({"successful":count},200)
             