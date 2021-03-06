from app import app
from app.UserManagement import UserManagement
from app.TestModule import TestModule
from app.NLP import NLP
from app.Content import Content
from app.RSSdb import RSSdb
from app.UserFavor import UserFavor

app.register_blueprint(UserManagement,url_prefix='/user')
app.register_blueprint(TestModule,url_prefix='/test')
app.register_blueprint(NLP,url_prefix='/nlp')
app.register_blueprint(Content, url_prefix='/content')
app.register_blueprint(UserFavor,url_prefix='/userfavor')
app.register_blueprint(RSSdb,url_prefix='/rssdb')