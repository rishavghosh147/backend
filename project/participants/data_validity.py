from marshmallow import Schema, fields, ValidationError,validates_schema

def validate_integer_length(n_digits):
    def validator(value):
        if value is None or len(str(value)) != n_digits:
            raise ValidationError(f'The integer must have exactly {n_digits} digits.')
    return validator

class EventName(Schema):
    event_name=fields.Str(required=True)

class TeamSchema(Schema):
    team = fields.String(required=False)
    team_leader=fields.String(required=False)
    id = fields.Integer(required=False)
    team_key=fields.Integer(validate=validate_integer_length(10),required=False)

    @validates_schema
    def team_or_id(self,data,**kwargs):
        if not (('team' in data and data['team']) or ('id' in data and 'team_key' in data)):
            raise ValidationError ("please enter valid input. Either 'team' or 'id' and 'team_key' !!!")

class Participate(Schema):
    event_name = fields.String(required=True)
    team_name = fields.Nested(TeamSchema, required=True)

class view_events(Schema):
    event_name=fields.Str(required=True)
    event_pic=fields.Str(required=True)
    event_date=fields.Str(required=True)
    about_event=fields.Str(required=True)
    coordinator=fields.Str(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    team=fields.Int(validate=validate_integer_length(1),required=True)

class view_winers(Schema):
    name=fields.Str(required=True)
    roll=fields.Int(validate=validate_integer_length(11),required=True)
    year=fields.Int(validate=validate_integer_length(1),required=True)
    stream=fields.Str(required=True)
    position=fields.Str(required=True)
    team_name=fields.Str(required=False)

class Team_winer(Schema):
    team_name=fields.String(required=True)
    marks=fields.Integer(required=True)

class Team_name(Schema):
    team_name=fields.String(required=True)

class Team_details(Schema):
    name=fields.String(required=True)
    stream=fields.String(required=True)
    year=fields.Integer(required=True)
    roll=fields.Integer(required=True)