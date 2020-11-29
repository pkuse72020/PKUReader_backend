from flask import Blueprint

UserManagement = Blueprint("UserManagement", __name__)

from app.UserManagement import routes
