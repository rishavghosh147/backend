from app import app
from flask import json,request, jsonify
from database.database import Event,db,Participants
from sqlalchemy import text
from authentication.token_validation import token_validation_admin
from flask_restful import Resource
import requests
from sqlalchemy import Column, String,Table

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg'}

class post_event(Resource): #done
    @token_validation_admin
    def post(self):
        if 'image' not in request.files :
         return jsonify({'error': 'Image data are required.'})

        event_pic = request.files['image']
        event_name=request.form['event_name']
        about_event=request.form['about_event']
        event_date=request.form['event_date']
        coordinetor=request.form['coordinetor']
        mobile=request.form['mobile']
        team=request.form['team']
        temp=Event.query.filter_by(event_name=event_name.lower()).first()

        if temp:
            return jsonify({'error':'the event already exist'})
        else:
            # event_pic.filename=event_name+event_pic.filename[-4:]
            # event_pic.save('images/'+event_pic.filename)
            link=post(event_pic)
            event=Event(event_name=event_name,event_date=event_date,about_event=about_event,team=team,event_pic=link,coordinetor=coordinetor,mobile=int(mobile))
            db.session.add(event)
            db.session.commit()
            return jsonify({'successful':'the event post successfully'})
        

def post(data):
        url = 'https://api.imgur.com/3/upload'
        access_token='413e9a80f0eb65ba363d1d8b4d7ca032a7754a13'
        headers = {'Authorization': f'Bearer {access_token}'}
        image = {'image': data.read()}
        response = requests.post(url, headers=headers, files=image)
        json_data = response.json()
        image_link = json_data['data']['link']
        return image_link




