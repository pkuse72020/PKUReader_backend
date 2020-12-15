from flask import Blueprint

NLP = Blueprint("NLP", __name__)

from app.NLP import routes
