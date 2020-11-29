from flask import Blueprint

UserManagement = Blueprint("UserManagement", __name__)

@UserManagement.route('/')
def hello_world():
    return "hello!"
