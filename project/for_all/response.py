from flask import jsonify,make_response

def resp(message,http_status_code):
    res=make_response(jsonify(message))
    res.status_code=http_status_code
    return res