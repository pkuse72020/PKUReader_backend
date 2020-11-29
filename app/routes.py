from app import app
from app.UserManagement import UserManagement
app.register_blueprint(UserManagement,url_prefix='/user')