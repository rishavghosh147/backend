from database.database import Participants,db,User,Event,Team_data,Team_participate
from flask import request
from authentication.token_validation import token_validation_participents,user_email
from flask_restful import Resource
from key.keys import participants_secret_key
from participants.data_validity import Participate as data_validity
from for_all.response import resp
from marshmallow import ValidationError
from authentication.send_otp import send_otp
import random

class Participate(Resource): #checked
    @token_validation_participents
    def post(self):
        marshmallow=data_validity()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        email=user_email(participants_secret_key)
        roll_obj=User.query.filter_by(email=email).first()
        event_type=Event.query.filter_by(event_name=data['event_name']).first()
        if event_type.team==1 and 'team_name' in data:
            check=db.session.query(Team_data).join(Team_participate,Team_participate.event_name==data['event_name']).filter(Team_data.roll==roll_obj.roll).first()
            if check is not None:return resp({"error":"you already participated !!!"},409)
            if 'team' in data['team_name']:
                check=Team_participate.query.filter_by(event_name=data['event_name'],team_name=data['team_name']['team']).first()
                if check is None:
                    team_key=random.randint(0000000000,9999999999)
                    leader=Team_participate(event_name=data['event_name'],team_name=data['team_name']['team'],team_key=team_key,team_leader=roll_obj.fname+" "+roll_obj.lname)
                    db.session.add(leader)
                    db.session.commit()
                    id=Team_participate.query.filter_by(event_name=data['event_name'],team_name=data['team_name']['team']).first()
                    participate(id.id,roll_obj.roll)
                    msg=f'you are registered successfully on {data["event_name"]} and your team id, team secret key is {id.id}, {team_key}'
                    send_otp(f'team details for {data["event_name"]}',email,msg)
                else: return resp({"error":"This team name already in use !!!"},409)
            elif 'id' in data['team_name'] and 'team_key' in data['team_name']:
                check=Team_participate.query.filter_by(event_name=data['event_name'],id=data['team_name']['id'],team_key=data['team_name']['team_key']).first()
                if check is not None:
                    participate(data['team_name']['id'],roll_obj.roll)
                else: return resp({"error":"please contact team leader for correct details !!!"},200)
        elif event_type.team==0:
            check=Participants.query.filter_by(roll=roll_obj.roll,event_name=data['event_name']).first()
            if check is None:
                event=Participants(roll=roll_obj.roll,event_name=data['event_name'])
                db.session.add(event)
                db.session.commit()
            else: return resp({"error":"you already participated !!!"},409)
        else: return resp({"error":"team_name is required !!!"},200)
        return resp({"successful":"participated successfully"}, 200)
    
def participate(id,roll):
    add_user=Team_data(_id=id,roll=roll)
    db.session.add(add_user)
    db.session.commit()