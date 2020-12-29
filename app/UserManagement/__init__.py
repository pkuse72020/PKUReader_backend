from flask import Blueprint

UserManagement = Blueprint("UserManagement", __name__)



from app.UserManagement import routes
from app.tables import UserInfo
from app import db


info = UserInfo("admin", "admin",True)
try:
    db.session.add(info)
    db.session.commit()
except Exception as e:
    db.session.rollback()
    print(e.args[0])