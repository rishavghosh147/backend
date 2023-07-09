from app import app
from flask import send_file, request

@app.route('/request_image/',methods=['POST'])
def request_image():
    data=request.json
    return send_file(data['image'], as_attachment=True)
