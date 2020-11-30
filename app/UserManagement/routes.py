from app.UserManagement import UserManagement
from flask import request, session, jsonify
from app.tables import UserInfo
from app import db, auth
from app.token_auth import generate_auth_token
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app import pubkey, privkey
import rsa


@UserManagement.route('/')
def hello_world():
    return "hello!"

# 注册
# 传入参数格式{"username":...,"password":...}
# 成功时返回参数格式{"state":"success","UserId":...}
# 失败时返回参数格式{"state":"failed","description":...}
@UserManagement.route('/signup', methods=["POST", "GET"])
def signip():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
    # username=rsa.decrypt(username,privkey).decode('utf-8')
    # password=rsa.decrypt(password,privkey).decode('utf-8')
    info = UserInfo(username, password)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"state": "failed", "description": e.args[0]})
    return jsonify({"state": "success", "UserId": info.UserId})

# 登陆
# 传入参数格式{"username":...,"password":...}
# 传入参数格式{"username":...,"password":...}
# 成功时返回参数格式{"state":"success","UserId":...,"token":...}
# 失败时返回参数格式{"state":"failed","description":...}
@UserManagement.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "GET":
        username = request.args.get("username")
        password = request.args.get("password")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
    # username=rsa.decrypt(username,privkey).decode('utf-8')
    # password=rsa.decrypt(password,privkey).decode('utf-8')
    try:
        result = UserInfo.query.filter_by(Username=username).all()
    except Exception as e:
        return jsonify({"state":"failed","description":e.args[0]})
    if (len(result) == 0):
        return jsonify({"state":"failed","description":"No such user."})
    if (len(result) != 1):
        return jsonify({"state": "failed", "description": "There are multiple lines in database with the same Username."})
    else:
        result = result[0]
        if result.checkPassword(password):
            return jsonify({"state": "success","UserId":result.UserId,"token":generate_auth_token(result.UserId,result.Password_hash)})
        else:
            return jsonify({"state": "failed", "description": "Wrong password."})
            

@UserManagement.route('/token_test', methods=["GET", "POST"])
@auth.login_required
def token_test():
    return "token success"


