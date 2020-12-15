from flask import Blueprint

TestModule = Blueprint("TestModule", __name__)

from app.TestModule import routes
