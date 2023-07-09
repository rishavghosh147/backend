from app import app
from flask import request, jsonify
from database.database import Crew

@app.route('/crew.py/',methods=['POST'])
def crew():
    data=request.json
    crews=Crew.query.filter_by(type=data[type]).all()
    return jsonify(crews)