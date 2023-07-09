from app import app
from database.database import Contact
from flask import jsonify

@app.route('/contact_us/',methods=['POST'])
def contact_us():
    contacts=Contact.query.all()
    return jsonify(contacts)