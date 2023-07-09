from app import app
from database.database import Coordinetor,db
from flask import request, jsonify

@app.route('/coordinators_request/',methods=['POST'])
def coordinators_request():
    users=Coordinetor.query.filter_by(status='pending').all()
    return jsonify(users)

@app.route('/request_approve/',methods=['POST'])
def request_approve():
    data=request.json
    user=Coordinetor.query.filter_by(email=data['email']).first()
    user.status='approved'
    db.session.commite()

@app.route('/request_delete/',methods='POST')
def request_delete():
    data=request.json
    db.session.delete(data['email'])
    db.session.commite()