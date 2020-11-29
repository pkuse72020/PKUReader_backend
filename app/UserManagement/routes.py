from app.UserManagement import UserManagement
from flask import request, session, jsonify
from app.tables import UserInfo
from app import db
from werkzeug.security import generate_password_hash,check_password_hash


@UserManagement.route('/')
def hello_world():
    return "hello!"


@UserManagement.route('/signup', methods=["POST", "GET"])
def signip():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
    info = UserInfo(username, password)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return e.with_traceback
    return jsonify({"state": "success", "UserId": info.UserId})


@UserManagement.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        userid = request.args.get("userid")
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        userid = request.form.get("userid")
        username = request.form.get("username")
        password = request.form.get("password")
    try:
        result = UserInfo.query.filter_by(UserId=userid).all()
    except Exception as e:
        return e.with_traceback
    if (len(result) == 0):
        return jsonify({"state":"failed","description":"No such user."})
    if (len(result) != 1):
        return jsonify({"state": "failed", "description": "There are multiple lines in database with the same Userid."})
    else:
        result = result[0]
        if username != result.Username:
            return jsonify({"state":"failed","description":"There is a conflict between your machine and the server. Your local cache file may be out-of-date."})
        password_hash = result.Password_hash
        if check_password_hash(password_hash, password):
            return jsonify({"state": "success"})
        else:
            return jsonify({"state":"failed","description":"Wrong password."})

