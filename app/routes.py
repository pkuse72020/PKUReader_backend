from app import app
from app.UserManagement import UserManagement
from app.TestModule import TestModule
from app.NLP import NLP


app.register_blueprint(UserManagement,url_prefix='/user')
app.register_blueprint(TestModule,url_prefix='/test')
app.register_blueprint(NLP,url_prefix='/nlp')



