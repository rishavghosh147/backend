from database.database import Event
from for_all.response import resp
from flask_restful import Resource
from participants.data_validity import view_events
from marshmallow import ValidationError

class veiw_events(Resource): #checked
    def post(self):
        events1=Event.query.all()
        events=[]
        for x in events1:
            events.append({
                "event_name":x.event_name,
                "event_pic":x.event_pic,
                "event_date":x.event_date,
                "about_event":x.about_event,
                "coordinator":x.coordinator,
                "mobile":x.mobile,
                "team":x.team})
        marshmallow=view_events(many=True)
        try:
            data=marshmallow.dumps(events)
        except ValidationError as e:
            return f'{e}'
        return resp(data,200)
   