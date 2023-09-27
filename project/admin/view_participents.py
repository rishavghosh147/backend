from flask import request
from authentication.token_validation import token_validation_admin
from database.database import Participants,User,db,Event,Team_participate,Team_data
from flask_restful import Resource
from admin.data_validity import EventName,view_participents
from for_all.response import resp
from marshmallow import ValidationError

class veiw_participents(Resource): #checked
    @token_validation_admin
    def post(self):
        marshmallow=EventName()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        return common(data)
    
def common(data):
    event=data['event_name'].lower()
    type=Event.query.filter_by(event_name=event).first()
    participants = []
    i=0
    if type.team==0:
        roll=Participants.query.filter_by(event_name=data['event_name']).all()
        for x in roll:
            user=User.query.filter_by(roll=roll[i].roll).first()
            i=i+1
            participants.append({
            'name': user.fname+" "+user.lname,
            'roll': user.roll,
            'email': user.email,
            'mobile': user.mobile,
            'year': user.year,
            'stream': user.stream})
    else:
        roll=db.session.query(Team_data).join(Team_participate,Team_participate.event_name==data['event_name']).filter(Team_data._id==Team_participate.id).all()
        for x in roll:
            user=User.query.filter_by(roll=roll[i].roll).first()
            team=db.session.query(Team_participate).join(Team_data,Team_participate.id==Team_data._id).filter_by(roll=user.roll).first()
            participants.append({
            'name': user.fname+" "+user.lname,
            'roll': user.roll,
            'email': user.email,
            'mobile': user.mobile,
            'year': user.year,
            'stream': user.stream,
            'team_name': team.team_name})
            
    marshmallow=view_participents(many=True)
    try:
        data=marshmallow.dumps(participants)
    except ValidationError as e:
        return f'{e}'
    return resp(data,200)
     