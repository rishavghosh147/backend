from app import app
from flask_mail import Mail, Message

app.config['SECRET_KEY']='bits2bytes2k23byrishavghosh'
app.config['MAIL_DEBUG'] = True

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TSL']=False
app.config['MAIL_USERNAME']='bits2bytes2k23@gmail.com'
app.config['MAIL_PASSWORD']='zcbairhkxqmdfsge'


mail=Mail(app)

def send_otp(subject,recipient,body):
    msg=Message(subject=subject,sender='bits2bytes2k23@gmail.com',recipients=[recipient])
    msg.body=body
    mail.send(msg)

def send_mail(subject,recipient,body,file):
    msg=Message(subject=subject,sender='bits2bytes2k23@gmail.com',recipients=[recipient])
    with app.open_resource(file) as fp:
        msg.attach(file.filename, 'application/octet-stream', fp.read())
    msg.body=body
    mail.send(msg)




 