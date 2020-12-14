from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from app.ArticleSearch import NewsElasticEngine
import rsa

app = Flask(__name__)


app.config['TOKEN_EXPIRATION'] = 30 * 24 * 3600
app.config['SECRET_KEY'] = 'k#6@1%8)a'
# 连接数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database.db'

# 设置是否跟踪数据库的修改情况，一般不跟踪
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_ECHO'] = True

auth = HTTPBasicAuth()

# 实例化orm框架的操作对象，后续数据库操作，都要基于操作对象来完成
db = SQLAlchemy(app)
es = NewsElasticEngine()

with open('private_key_file.pem', mode='rb') as privfile:
    keydata = privfile.read()
privkey = rsa.PrivateKey.load_pkcs1(keydata)
with open('public_key_file.pem', mode='rb') as privfile:
    keydata = privfile.read()
pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)


from app import routes
from app.tables import *
from app.token_auth import *




