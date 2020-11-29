from app.UserManagement import UserManagement
from flask import jsonify

@UserManagement.route('/')
def hello_world():
    return "hello!"


# 调用自定义包: datatime, 具体路径在run.py同目录下的文件夹中
from datatime.get_time import get_now_time
@UserManagement.route('/time')
def hello_time():
    out_json = {'time':get_now_time()}
    return jsonify(out_json)

# 调用自定义db包，进行数据库操作
from db.user_db import UserDB
userdb = UserDB()
@UserManagement.route('/getTable')
def hello_user():
    all_users = userdb.selectAllUser()
    out_json = {'msg':all_users}
    return jsonify(out_json)