from app import db
from werkzeug.security import generate_password_hash, check_password_hash
import uuid


class UserInfo(db.Model):
    __tablename__ = "UserInfo"
    UserId = db.Column(db.String(100), nullable=False,
                       unique=True, primary_key=True)
    Username = db.Column(db.String(20), nullable=False, unique=True)
    # Password = db.Column(db.String(20), nullable=True)
    Password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.UserId = str(uuid.uuid1())
        self.Username = username
        self.Password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.Password_hash, password)

class FocusArticle(db.Model):
    '''
    Focus of Articles
    '''
    __tablename__ = "FocusArticle"
    FAId = db.Column(db.String(100), nullable=False,
                     unique=True, primary_key=True)
    UserId = db.Column(db.String(100), db.ForeignKey('UserInfo.UserId'))
    ArticleId = db.Column(db.String(100))
    #user = db.relationship("UserInfo", back_populates="FocusArticle")
    def __init__(self, _userid, _articleid):
        self.FAId = str(uuid.uuid4())
        self.UserId = _userid
        self.ArticleId = _articleid

class FocusFeed(db.Model):
    '''
    Focus of Feed
    '''
    __tablename__ = "FocusFeed"
    FFId = db.Column(db.String(100), nullable=False,
                     unique=True, primary_key=True)
    UserId = db.Column(db.String(100), db.ForeignKey('UserInfo.UserId'))
    RSSTitle = db.Column(db.String(100))
    RSSurl = db.Column(db.String(200))
    #user = db.relationship("UserInfo", back_populates="FocusFeed")

    def __init__(self, _userid, _title, _url):
        self.FFId = str(uuid.uuid4())
        self.UserId = _userid
        self.RSSTitle = _title
        self.RSSurl = _url



class Article(db.Model):
    __tablename__ = "Article"
    ArticleId = db.Column(db.String(100), nullable=False,
                          unique=True, primary_key=True)
    ArticleTitle = db.Column(db.String(100), nullable=False, unique=True)
    ArticleContent = db.Column(db.String(10000))

    def __init__(self, _title, _content):
        self.ArticleId = str(uuid.uuid4())
        self.ArticleTitle = _title
        self.ArticleContent = _content


class Article2Keyword(db.Model):
    __tablename__ = "Article2Keyword"
    A2Kid = db.Column(db.String(100), nullable=False,
                      unique=True, primary_key=True)
    ArticleId = db.Column(db.String(100), db.ForeignKey("Article.ArticleId"))
    #article = db.relationship("Article", back_populates="Article2Keyword")
    #ArticleId = db.Column(db.String(100))
    Keyword = db.Column(db.String(100))

    def __init__(self, _articleid, _keyword):
        self.A2Kid = str(uuid.uuid4())
        self.ArticleId = _articleid
        self.Keyword = _keyword

