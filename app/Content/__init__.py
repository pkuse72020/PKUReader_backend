from flask import Blueprint

Content = Blueprint("Content", __name__)

from app.Content import routes