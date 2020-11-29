from app import db
from werkzeug.security import generate_password_hash,check_password_hash


class UserInfo(db.Model):
    __tablename__="UserInfo"
    UserId = db.Column(db.Integer, nullable=False,
                       unique=True, primary_key=True)
    Username = db.Column(db.String(20), nullable=False)
    # Password = db.Column(db.String(20), nullable=True)
    Password_hash=db.Column(db.String(100),nullable=False)

    def __init__(self, username, password):
        self.UserId=len(UserInfo.query.all())+1
        self.Username = username
        self.Password_hash = generate_password_hash(password)
    def checkPassword(self, password):
        return check_password_hash(self.Password_hash, password)