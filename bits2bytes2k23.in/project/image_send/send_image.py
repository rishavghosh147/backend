from app import app
from flask import send_file,request,json,send_from_directory
from flask_restful import Resource
from authentication.return_respose import response

class send_image(Resource): #done
    def post(self):
        image=json.loads(request.data)
        return response(send_from_directory('images',image['event_pic'], as_attachment=True),200)
