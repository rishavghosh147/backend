from app import app
from database.database import Participants,Team_participate,db,Event,User
from flask_restful import Resource
from flask import json,request,jsonify
import jwt
from key.keys import participants_secret_key,authorization_token_key
from authentication.token_validation import token_validation_participents,user_email

class praricipated_or_not(Resource): #done
    @token_validation_participents
    def post(self):
        data=json.loads(request.data)
        email=user_email(participants_secret_key)
        roll=User.query.filter_by(email=email).first()
        event=Event.query.filter_by(event_name=data['event_name']).first()
        if event.team==1:
            user=Team_participate.query.filter_by(roll=roll.roll).filter(Team_participate.event_name==data['event_name']).first()
            if user:
                return jsonify({"successful":1})
            else:
                return jsonify({"error":0})
        else:
            user=Participants.query.filter(Participants.roll==roll.roll,Participants.event_name==data['event_name']).first()
            if user:
                return jsonify({"successful":1})
            else:
                return jsonify({"error":0})