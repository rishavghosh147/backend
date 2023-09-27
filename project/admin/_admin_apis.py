from flask import Blueprint
from flask_restful import Api
from admin.delete_user import delete_user
from admin.download_data import Download_by_admin
from admin.view_deleted_user import veiw_deleted_user
from admin.post_event import post_event
from admin.view_deleted_user import veiw_deleted_user
from admin.view_participents import veiw_participents
from admin.all_participants import users
from admin.view_event import veiw_events
from admin.post_winers import winers 

_admin=Blueprint("admin",__name__,url_prefix="/admin")

api=Api(_admin)

api.add_resource(veiw_deleted_user,'/view_deleted_user/') #the api is for veiw the deleted user 
api.add_resource(delete_user,'/delete_user/') #this api is for delete participants
api.add_resource(post_event,'/post_event/') #this api is for post the events
api.add_resource(veiw_participents,'/view_participents/') #this api is for veiw the participants
api.add_resource(Download_by_admin,'/download_by_admin/') #this api is for download participants details on a particular event
api.add_resource(winers,'/post_winers/') #this api is for post winer by admin
api.add_resource(users,'/all_users/') #this api is for fetch all the users
api.add_resource(veiw_events,'/view_event/') #to veiw all the event

