from flask_restful import Resource
from flask import request
from database.database import Winers,User,Event,Team_participate
from participants.data_validity import EventName,Team_winer
from for_all.response import resp
from participants.data_validity import view_winers
from marshmallow import ValidationError

class win(Resource): #done
    def post(self):
        marshmallow=EventName()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        event=Event.query.filter_by(event_name=data['event_name']).first()
        win=[]
        if event.team==0:
            winers=Winers.query.filter_by(event_name=data['event_name']).order_by(Winers.marks.desc()).all()
            for x in winers:
                user=User.query.filter_by(roll=x.roll).first()
                win.append(
                    {"name":user.fname+" "+user.lname,
                    "roll":x.roll,
                    "year":user.year,
                    "stream":user.stream,
                    "marks":x.winers})
            marshmallow=view_winers(many=True)
            try:
                data=marshmallow.dumps(win)
            except ValidationError as e:
                return f'{e}'
        else:
            winer=Winers.query.filter_by(event_name=data['event_name']).order_by(Winers.marks.desc()).all()
            for x in winer:
                win.append({
                        "team_name":x.team_name,
                        "marks":x.marks
                    })
                marshmallow=Team_winer(many=True)
                try:
                    data=marshmallow.dumps(win)
                except ValidationError as e:
                    return f'{e}'
        return resp(data,200)
        