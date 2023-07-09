from app import app
from database.database import User
from flask import request, jsonify

@app.route('/register/',methods=['POST'])
def register():
    data=request.json
    validity=check_data(data)
    if validity:
        exist=User.query.filter((User.email==data['email'])|(User.mobile==data['mobile'])|(User.roll==data['roll'])).all()
        if exist !=None:
            return jsonify({'message':'user already exist !!!'})
        else:
            ...
            # return !          !!!!!!
    else:
        return jsonify({'message':'data is incomplete'})


def check_data(data):
    if len(data)==8 and data['fname'] and data['lname'] and data['mobile'] and data['email'] and data['roll'] and data['stream'] and data['year'] and data['password']:
        return True
    else:
        False

