from app.UserManagement import UserManagement
from flask import jsonify

@UserManagement.route('/')
def hello_world():
    return "hello!"
