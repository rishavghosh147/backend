from app import app
from database.database import Participents
from flask import jsonify

@app.route('/coordinetor/participents/',methods=['POST'])
def coordinetor_view():
    event_name='event_name'
    users=Participents.query.filter_by(evente_name=1).all()
    return jsonify(users)