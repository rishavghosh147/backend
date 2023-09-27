from marshmallow import Schema, fields, ValidationError, validates_schema

def validate_integer_length(n_digits):
    def validator(value):
        if value is None or len(str(value)) != n_digits:
            raise ValidationError(f'The integer must have exactly {n_digits} digits.')
    return validator

class DeleteUser(Schema):      #this is for delete_user
    roll=fields.Integer(validate=validate_integer_length(11), required=True)

class EventName(Schema):       #this is for download_data and view_event
    event_name=fields.String(required=True)

class PostEvent(Schema):       #this is for post_event
    event_name=fields.String(required=True)
    about_event=fields.String(required=True)
    event_date=fields.String(required=True)
    coordinator=fields.String(required=True)
    mobile=fields.Integer(validate=validate_integer_length(10),required=True)
    team=fields.Integer(validate=validate_integer_length(1),required=True)

    @validates_schema
    def roll_or_team(self,data,**kwargs):
        if not (data.get('team')==0 or data.get('team')==1):
            raise ValidationError ("please enter team either '0' or '1'")

class PostWiners(Schema):       #this is for post_winers
    marks=fields.Integer(validate=validate_integer_length(2),required=True)
    roll=fields.Integer(validate=validate_integer_length(11),required=False)
    team_name=fields.Str(required=False)
    event_name=fields.String(required=True)

    @validates_schema
    def roll_or_team(self,data,**kwargs):
        if not data.get('roll') or data.get('team_name'):
            raise ValidationError('Either "roll" or "team_name" field is required.')
     
class all_participants(Schema):
    fname=fields.Str(required=True)
    lname=fields.Str(required=True)
    email=fields.Email(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    roll=fields.Int(validate=validate_integer_length(11),required=True)
    stream=fields.Str(required=True)
    year=fields.Int(validate=validate_integer_length(1))

class view_deleted_user(Schema):
    fname=fields.Str(required=True)
    lname=fields.Str(required=True)
    email=fields.Email(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    roll=fields.Int(validate=validate_integer_length(11),required=True)
    stream=fields.Str(required=True)
    year=fields.Int(validate=validate_integer_length(1))
    deleted_by=fields.Email(required=True)

class view_participents(Schema):
    name=fields.Str(required=True)
    email=fields.Email(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    roll=fields.Int(validate=validate_integer_length(11),required=True)
    stream=fields.Str(required=True)
    year=fields.Int(validate=validate_integer_length(1))
    team_name=fields.Email(required=False)