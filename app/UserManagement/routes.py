from app.UserManagement import UserManagement
from flask import request, session
from app.tables import UserInfo
from app import db


@UserManagement.route('/')
def hello_world():
    return "hello!"


@UserManagement.route('/signup', methods=["POST","GET"])
def signip():
    username = request.args.get("username")
    password = request.args.get("password")
    info = UserInfo(username,password)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e.with_traceback
    return "success"
