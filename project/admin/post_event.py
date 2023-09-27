from flask import request, json
from database.database import Event,db
from authentication.token_validation import token_validation_admin
from flask_restful import Resource
import requests
from admin.data_validity import PostEvent
from for_all.response import resp
from marshmallow import ValidationError

class post_event(Resource): #checked
    @token_validation_admin
    def post(self):
        if not 'event_pic' in request.files: return resp({"error":"image not present in data !!!"}, 406)
        event_pic = request.files['event_pic']
        data=request.form.to_dict()

        marshmallo=PostEvent()
        try:
            data=marshmallo.loads(json.dumps(data))
        except ValidationError as e:
            return resp({'error':e.messages},406)
        
        temp=Event.query.filter_by(event_name=data['event_name'].lower()).first()
        if temp:
            return resp({'error':'the event already exist'},409)
        else:
            # event_pic.filename=event_name+event_pic.filename[-4:]
            # event_pic.save('images/'+event_pic.filename)
            # link="https://i.imgur.com/8LYM8ZK.jpeg"
            link=save_image(event_pic)
            event=Event(event_name=data['event_name'],event_date=data['event_date'],about_event=data['about_event'],team=data['team'],event_pic=link,coordinator=data['coordinator'],mobile=data['mobile'])
            db.session.add(event)
            db.session.commit()
            return resp({'successful':'the event post successfully'},200)
        

def save_image(data):
        url = 'https://api.imgur.com/3/upload'
        access_token='e0f1a7590871610628203de6838c4cf8093e636a'
        headers = {'Authorization': f'Bearer {access_token}'}
        image = {'image': data.read()}
        response = requests.post(url, headers=headers, files=image)
        json_data = response.json()
        image_link = json_data['data']['link']
        return image_link