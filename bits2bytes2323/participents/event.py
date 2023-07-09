from app import app
from database.database import Event
from flask import jsonify

@app.route('/events/',methods=['POST'])
def events():
    events=Event.query.all()
    return jsonify(events)

