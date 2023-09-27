from flask_restful import Resource
from participants.data_validity import Team_name, Team_details as details
from flask import request
from marshmallow import ValidationError
from database.database import Team_participate,Team_data,User
from for_all.response import resp

class Team_details(Resource):
    def post(self):
        marshmallow=Team_name()
        try:
            data=marshmallow.loads(request.data)
        except ValidationError as e:
            return f'{e}'
        id=Team_participate.query.filter_by(team_name=data['team_name']).first()
        rolls=Team_data.query.filter_by(_id=id.id).all()
        team=[]
        for roll in rolls:
            user=User.query.filter_by(roll=roll.roll).first()
            team.append({
                "name":user.fname+" "+user.lname,
                "stream": user.stream,
                "year":user.year,
                "roll":user.roll
            })
        marshmallow1 = details(many=True)
        try:
            return resp(marshmallow1.dumps(team),200)
        except ValidationError as e:
            return f'{e}'