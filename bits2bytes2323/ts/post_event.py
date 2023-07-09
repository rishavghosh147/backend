from app import app
from flask import request, json
from database.database import Event

@app.route('/post_event/',methods=['POST'])
def post_event():
    image=request.files['event_image']
    data=request.form["json"]
    data=json.loads(data)
    image.filename=data['event_name']+image.filename[-4:]
    image.save('event_image/'+image.filename)
    check=Event.query.filter_by('event_name').first()
    if check==None:
        event=Event(event_name=data['event_name'],event_type=data['event_type'],about_event=data['about_event'],start_date=data['start_date'],event_image=data['event_image'])
        return 'success'
    else:
        return 'already exits'