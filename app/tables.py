from app import db


class UserInfo(db.Model):
    __tablename__="UserInfo"
    UserId = db.Column(db.Integer, nullable=False,
                       unique=True, primary_key=True)
    Username = db.Column(db.String(20), nullable=False)
    Password = db.Column(db.String(20), nullable=False)

    def __init__(self, username, password):
        self.UserId=len(UserInfo.query.all())+1
        self.Username = username
        self.Password = password