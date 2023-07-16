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
    # @token_validation_admin
    def post(self):
        event_pic = request.files['event_pic']
        event_name=request.form['event_name']
        about_event=request.form['about_event']
        event_date=request.form['event_date']
        coordinator=request.form['coordinator']
        mobile=request.form['mobile']
        team=request.form['team']
        
        temp=Event.query.filter_by(event_name=event_name.lower()).first()
        if temp:
            return jsonify({'error':'the event already exist'})
        else:
            # event_pic.filename=event_name+event_pic.filename[-4:]
            # event_pic.save('images/'+event_pic.filename)
            link=post(event_pic)
            # link="https://i.imgur.com/8LYM8ZK.jpeg"
            event=Event(event_name=event_name,event_date=event_date,about_event=about_event,team=team,event_pic=link,coordinator=coordinator,mobile=int(mobile))
            db.session.add(event)
            db.session.commit()
            return jsonify({'successful':'the event post successfully'})
        

def post(data):
        url = 'https://api.imgur.com/3/upload'
        access_token='e0f1a7590871610628203de6838c4cf8093e636a'
        headers = {'Authorization': f'Bearer {access_token}'}
        image = {'image': data.read()}
        response = requests.post(url, headers=headers, files=image)
        json_data = response.json()
        image_link = json_data['data']['link']
        return image_link




