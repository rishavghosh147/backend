from flask_restful import Resource
from flask import request
from authentication.token_validation import token_validation_admin, user_email
from database.database import Event,Team_participate,Participants,User,db
import pandas as pd
from authentication.send_otp import send_mail
from key.keys import admin_secret_key
from for_all.response import resp
from admin.data_validity import EventName

class Download_by_admin(Resource): # !!!!
    @token_validation_admin
    def post(self):
        marshmallow=EventName()
        try:
            data=marshmallow.loads(request.data)
        except ValueError as e:
            return resp({'error':e.messages},406)
        event=Event.query.filter_by(event_name=data['event_name']).first()
        xl=[]
        if event:
            if event.team==0:
                roll=Participants.query.filter_by(event_name=data['event_name']).all()
                for i,x in enumerate(roll):
                    user=User.query.filter_by(roll=roll[i].roll).first()
                    xl.append({
                    'name': user.fname+" "+user.lname,
                    'roll': user.roll,
                    'email': user.email,
                    'mobile': user.mobile,
                    'year': user.year,
                    'stream': user.stream
                })
            else:
                roll=Team_participate.query.filter_by(event_name=data['event_name']).order_by(Team_participate.team_name).all()
                # roll=db.session.query() !!!
                for x in roll:
                    user=User.query.filter_by(roll=roll[i].roll).first()
                    xl.append({
                    'name': user.fname+" "+user.lname,
                    'roll': user.roll,
                    'email': user.email,
                    'mobile': user.mobile,
                    'year': user.year,
                    'stream': user.stream, 
                    'team_name': x.team_name
                })
                    
            filename='event_details/'+data['event_name']+'.xlsx'
            df=pd.DataFrame(xl)
            df.to_excel(filename,index=False)
            msg=f"Participants of {data['event_name']}"
            email=user_email(admin_secret_key)
            send_mail('Participants details',email,msg)
            return resp({"successful":"please check your mail"}, 200)