from flask import make_response

def response(response,status_code):
    response.status_code = status_code
    return response