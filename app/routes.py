from app import app
from app.UserManagement import UserManagement
from app.TestModule import TestModule


app.register_blueprint(UserManagement,url_prefix='/user')
app.register_blueprint(TestModule,url_prefix='/test')



