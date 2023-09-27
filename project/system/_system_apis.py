from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS

from system.login import User_login
from system.sign_up import user_signup
from system.forget_password import forget_password
from system.otp_verify import otp_verify
from system.view_profile import veiw_profile
from system.resend_otp import resend_otp
from system.update_profile import update_profile
from system.user_type import User_type

_system=Blueprint("system",__name__,url_prefix="/system")

api=Api(_system)

api.add_resource(User_login,'/login/') #this api is used for user login
api.add_resource(user_signup,'/user_signup/') #this api is used for user sign up
api.add_resource(otp_verify,'/otp_verify/') #this otp is for otp verification of login and sign up
api.add_resource(forget_password,'/forget_password/') #this api is for forget the password
api.add_resource(veiw_profile,'/view_profile/') #this api is for veiw participants profile veiw
api.add_resource(resend_otp,'/resend_otp/') #this api is for resend the otp
api.add_resource(update_profile,'/update_profile/') #this api is for update participants profile
api.add_resource(User_type,'/user_type/') #this api is for check the user admin or participant

#  ****** cors is very important to connect with fontend
CORS(_system, resources={r"/*":{"origins": "*"}}, methods=['POST'], allow_headers=['Content-Type','Access-Control-Allow-Origin','Authorization','verification'])