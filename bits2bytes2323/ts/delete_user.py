from app import app
from flask import request,jsonify
from database.database import User, Parricipents,db

@app.route('/delete_user/',methods=['POST'])
def delete_user():
    data=request.json
    key=list(data.keys())
    user_check=User.query.filter_by(key=data[key]).first()
    if user_check is not None:
        participetion_check=Parricipents.query.filter_by(user=user_check).first()
        if participetion_check is not None:
            db.session.delete(participetion_check)
            db.session.commit()
        db.session.delete(user_check)
        db.session.commit()
        return jsonify({'message':'user deleted successfully'})
    else:
        return jsonify({'message':'user not exists'})