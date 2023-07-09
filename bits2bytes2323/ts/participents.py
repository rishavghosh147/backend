from app import app
from flask import request, jsonify
from database.database import Parricipents

@app.route('/participents/',methods='POSt')
def participents():
    data=request.json
    data=data['event_name']
    user=Parricipents.query.filter_by(data=1).all()
    return jsonify(user)