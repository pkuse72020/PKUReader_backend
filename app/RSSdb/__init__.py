from flask import Blueprint

RSSdb = Blueprint("RSSdb", __name__)

from app.RSSdb import routes
