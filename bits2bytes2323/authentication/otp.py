from app import app
from flask_mail import Mail, Message
import pyotp

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'rishavghosh148@gmail.com'
app.config['MAIL_PASSWORD'] ='bcogzqcnrndjdsiy'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail=Mail(app)

def send_otp(user,type):
    msg=Message(user,sender='rishavghosh148@gmail.com',recipients=[type])
    totp=pyotp.TOTP(pyotp.random_base32())
    otp=totp.now()
    msg.body='The OTP for registration in bits2bytes2k23 is '+otp
    mail.send(msg)
    return otp