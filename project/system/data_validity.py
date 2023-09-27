from marshmallow import Schema, fields, validates_schema, ValidationError
from key.keys import len_of_secret_key

def validate_integer_length(n_digits):
    def validator(value):
        if value is None or len(str(value)) != n_digits:
            raise ValidationError(f'The integer must have exactly {n_digits} digits.')
    return validator

class ForgetPassword(Schema):
    email=fields.Email(required=False)
    roll=fields.Int(validate=validate_integer_length(11),required=False)
    password=fields.Str(required=True)

    @validates_schema
    def roll_or_team(self,data,**kwargs):
        if not (data.get('roll') or data.get('email')):
            raise ValidationError('Either "roll" or "email" field is required.')

class Otp(Schema):
    otp=fields.Int(validate=validate_integer_length(6),required=True)

class SignUp(Schema):
    fname=fields.Str(required=True)
    lname=fields.Str(required=True)
    email=fields.Email(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    password=fields.Str(validate=validate_integer_length(8),required=True)
    secret_key=fields.Int(validate=validate_integer_length(len_of_secret_key),required=False)
    roll=fields.Int(validate=validate_integer_length(11),required=False)
    stream=fields.Str(required=False)
    year=fields.Int(validate=validate_integer_length(1),required=False)

    @validates_schema
    def admin_or_participants(self,data,**kwargs):
        if not (data.get('secret_key') or (data.get('roll') and data.get('stream') and data.get('year'))):
            raise ValidationError('Please enter a valid data !!!')
    
class UpdateProfile(Schema):
    fname=fields.Str(required=True)
    lname=fields.Str(required=True)
    mobile=fields.Int(validate=validate_integer_length(10),required=True)
    stream=fields.Str(required=False)
    year=fields.Int(validate=validate_integer_length(1),required=False)
