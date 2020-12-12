from flask import Blueprint

UserFavor = Blueprint("UserFavor", __name__)

from app.UserFavor import routes
