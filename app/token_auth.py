from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app import app,auth
from app.tables import UserInfo
from flask import jsonify



def generate_auth_token(UserId,Password_hash):
    s = Serializer(app.config['SECRET_KEY'], expires_in=app.config['TOKEN_EXPIRATION'])
    token = s.dumps({UserId: Password_hash})
    return token.decode("ascii")
 
 
@auth.verify_password
def verify_auth_token(token, password):  # 注意只能两个参数
    """验证token"""
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)  
    except SignatureExpired:
        # raise SignatureExpired('令牌已过期')
        return False
    except BadSignature:
        return False
    return True
 
