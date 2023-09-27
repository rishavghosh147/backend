from flask import Blueprint
from flask_restful import Api

from participants.participate_event import Participate
from participants.view_events import veiw_events
from participants.no_of_participants import no_of_participants
from participants.participated_or_not import praricipated_or_not
from participants.view_winers import win
from participants.team_details import Team_details

_participants=Blueprint("participants",__name__,url_prefix="/participants")

api=Api(_participants)

api.add_resource(veiw_events,'/view_event/') #to veiw all the event
api.add_resource(Participate,'/participate/') #participate any event
api.add_resource(praricipated_or_not,'/participated_or_not/') #this api is for check the participant is participated or not on a particular event
api.add_resource(no_of_participants,'/no_of_participants/') #this api is for find the no of participants on a particular event
api.add_resource(win,'/view_winers/') #this api is for veiw the winer of a particular event
api.add_resource(Team_details,'/team_details/') #this api is for team details