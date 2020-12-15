from flask import json
from flask.json import jsonify
from app import db
import uuid

import app
from app.tables import *

'''
created by zkc
start>>>>>>>>>>>>>>>>>>>
'''
# https://www.cnblogs.com/RanchoLi/p/8351924.html
class KnownRSS(db.Model):
    '''
    knownRSS_DB: rssId, rsslink, rsstitle
    '''
    __tablename__ = "KnownRSS"
    rssId = db.Column(db.Integer, primary_key=True)
    rsslink = db.Column(db.String(100), nullable=False, unique=True)
    # Password = db.Column(db.String(20), nullable=True)
    rsstitle = db.Column(db.String(100), nullable=False)


    def __init__(self, rsslink, rsstitle):
        self.rsslink = rsslink
        self.rsstitle = rsstitle

class FavorRSS(db.Model):
    '''
    FavorRSS_DB: rssId, rsslink, rsstitle
    '''
    __tablename__ = "FavorRSS"
    _Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    # Password = db.Column(db.String(20), nullable=True)
    rssId = db.Column(db.Integer, nullable=False)

    def __init__(self, userId, rssId):
        self.userId = userId
        self.rssId = rssId

class FavorArticle(db.Model):
    '''
    FavorArticle_DB: rssId, rsslink, rsstitle
    '''
    __tablename__ = "FavorArticle"
    _Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    # Password = db.Column(db.String(20), nullable=True)
    articleId = db.Column(db.String(100))

    def __init__(self, userId, articleId):
        self.userId = userId
        self.articleId = articleId


class pendingMsg(db.Model):
    '''
    pendingMsg_DB: rssId, rsslink, rsstitle
    '''
    __tablename__ = "pendingMsg"
    _Id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.String(100), nullable=False)
    rsstitle = db.Column(db.String(100), nullable=False)
    rsslink = db.Column(db.String(100), nullable=False)
    checkedByAdministrator = db.Column(db.String(100))

    def __init__(self, userId, rsstitle, rsslink):
        self.userId = userId
        self.rsstitle = rsstitle
        self.rsslink = rsslink
        self.checkedByAdministrator = "None"




'''
functions
'''

# 两个函数，用于将flask_sql的输出转化为可以直接网络传输的json格式
# 用法：直接调用classlist2dictlist，输入可以是单个object或者多个object的列表
def class2dict(class_entry):
    ret = {}
    remove_keys = ['_sa_instance_state']
    for e in class_entry.__dict__:
        if e in remove_keys:
            continue
        ret[e] = class_entry.__dict__[e]
    return ret

def classlist2dictlist(class_entries):
    if type(class_entries) != type([]):
        class_entries = [class_entries]
    ret_list = [class2dict(e) for e in class_entries]
    return ret_list


# 用户收藏一篇文章
def userAddFavorArticle(userId, articleId):
    try:
        result = FavorArticle.query.filter_by(userId = userId, articleId = articleId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    
    if len(result) != 0:
        return jsonify({'state':'failed', "description": "first query existed", "moreMsg":classlist2dictlist(result)})

    info = FavorArticle(userId, articleId)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'state':'failed', "description": "second query failed with error: " + str(e.args[0])})
    
    try:
        result = FavorArticle.query.filter_by(userId = userId, articleId = articleId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    if len(result) == 0:
        return jsonify({'state':'failed', "description": "third query failed with no queryMsg"})
    else:
        return jsonify({"state":'success', "description": "success", "moreMsg":classlist2dictlist(result)})

# 用户获得所有收藏的文章id
def userGetFavorArticles_id(userId):
    try:
        result = FavorArticle.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
    # return [{'_Id':e._Id,'userId':e.userId, "articleId":e.articleId} for e in result]


def getArticleByID(articleid, other_info = {}):
    try:
        article_rst = Article.query.filter_by(ArticleId=articleid).all()
    except Exception as e:
        return None
    if len(article_rst) == 0:
        return None
    cur_article = article_rst[0]

    keywordlist = Article2Keyword.query.filter_by(ArticleId=articleid).all()
    keywordlist = [x.Keyword for x in keywordlist]
    keywordlist = dict(zip(range(len(keywordlist)), keywordlist))
    
    _Id = 1
    userId = "test_user"

    if '_Id' in other_info:
        _Id = other_info['_Id']
    if 'userId' in other_info:
        userId = other_info['userId']

    return {
        'title': cur_article.ArticleTitle,
        'content': cur_article.ArticleContent,
        'keywords': keywordlist,
        '_Id':_Id,
        'userId':userId,
        'articleId':articleid
    }

def userGetFavorArticles(userId):
    try:
        result = FavorArticle.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    rst = classlist2dictlist(result)

    article_contents = [getArticleByID(e['articleId'],e) for e in rst]

    return jsonify({'state':'success', "rst":article_contents})
    # return [{'_Id':e._Id,'userId':e.userId, "articleId":e.articleId} for e in result]


# 用户移除一篇收藏的文章
def userRemoveFavorArticle(userId, articleId):
    try:
        result = FavorArticle.query.filter_by(userId = userId, articleId = articleId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})

# 用户增加一个RSS订阅
def userAddFavorRSS(userId, RSSId):
    try:
        result = FavorRSS.query.filter_by(userId = userId, rssId = RSSId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    
    if len(result) != 0:
        return jsonify({'state':'failed', "description": "first query existed", "moreMsg":classlist2dictlist(result)})

    info = FavorRSS(userId, RSSId)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'state':'failed', "description": "second query failed with error: " + str(e.args[0])})
    
    try:
        result = FavorRSS.query.filter_by(userId = userId, rssId = RSSId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    if len(result) == 0:
        return jsonify({'state':'failed', "description": "third query failed with no queryMsg"})
    else:
        return jsonify({"state":'success', "description": "success", "moreMsg":classlist2dictlist(result)})

# 用户获得所有已经订阅的RSS的id
def userGetFavorRSSs(userId):
    try:
        result = FavorRSS.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
    # return [{'_Id':e._Id,'userId':e.userId, "rssId":e.rssId} for e in result]


# 用户获得所有订阅的RSS的link和title
def userGetFavorRSS_links(userId):
    try:
        result = FavorRSS.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    rst = classlist2dictlist(result)
    try:
        allrss_rst = KnownRSS.query.all()
        allrss_rst = classlist2dictlist(allrss_rst)
    except Exception as e:
        return jsonify({'state':'failed', "description": str(e.args[0])})
    
    try:
        all_rss = allrss_rst
        rssid2rsslink = {e['rssId']:e['rsslink'] for e in all_rss}
        rssid2rsstitle = {e['rssId']:e['rsstitle'] for e in all_rss}
        rst = [{'_Id':e['_Id'], 'userId':e['userId'], 'rsslink':rssid2rsslink[e['rssId']],'rsstitle':rssid2rsstitle[e['rssId']], 'rssId':e['rssId']} for e in rst]
        return jsonify({'state':'success', "rst":rst})
    except Exception as e:
        return jsonify({'state':'failed', "description": str(e.args[0])})

# 返回对象
def userGetFavorRSS_links_obj(userId):
    try:
        result = FavorRSS.query.filter_by(userId=userId).all()
    except Exception as e:
        return {'state': 'failed', "description": "first query failed with error: " + str(e.args[0])}
    rst = classlist2dictlist(result)
    try:
        allrss_rst = KnownRSS.query.all()
        allrss_rst = classlist2dictlist(allrss_rst)
    except Exception as e:
        return {'state': 'failed', "description": str(e.args[0])}

    try:
        all_rss = allrss_rst
        rssid2rsslink = {e['rssId']: e['rsslink'] for e in all_rss}
        rssid2rsstitle = {e['rssId']: e['rsstitle'] for e in all_rss}
        rst = [{'_Id': e['_Id'], 'userId': e['userId'], 'rsslink': rssid2rsslink[e['rssId']],
                'rsstitle': rssid2rsstitle[e['rssId']]} for e in rst]
        return {'state': 'success', "rst": rst}
    except Exception as e:
        return {'state': 'failed', "description": str(e.args[0])}

# 用户移除一个RSS订阅
def userRemoveFavorRSS(userId, RSSId):
    try:
        result =  FavorRSS.query.filter_by(userId = userId, rssId = RSSId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})

# 用户提交一个rss申请请求
def addPendingMsg(userId, rsstitle, rsslink):
    try:
        rsslink_result = KnownRSS.query.filter_by(rsslink = rsslink).all()
        rsstitle_result = KnownRSS.query.filter_by(rsstitle = rsstitle).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    if len(rsslink_result) != 0:
        return jsonify({'state':'failed', "description": "first query existed with rsslink", "moreMsg":classlist2dictlist(rsslink_result)})
    if len(rsstitle_result) != 0:
        return jsonify({'state':'failed', "description": "first query existed with rsstitle", "moreMsg":classlist2dictlist(rsstitle_result)})

    info = pendingMsg(userId, rsstitle, rsslink)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'state':'failed', "description": "second query failed with error: " + str(e.args[0])})
    
    try:
        result = pendingMsg.query.filter_by(userId = userId, rsstitle = rsstitle, rsslink = rsslink).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    if len(result) == 0:
        return jsonify({'state':'failed', "description": "third query failed with no queryMsg"})
    else:
        # print(result[0].__dict__)
        return jsonify({"state":'success', "description": "success", "moreMsg":classlist2dictlist(result)})

# 管理员获得所有请求队列中未审核的内容
def getPendingMsg(administratorId):
    try:
        result = pendingMsg.query.filter(pendingMsg.checkedByAdministrator == "None").all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})

# 管理员直接增加一个knownRSS数据记录
def addKnownRSS(rsslink, rsstitle):
    try:
        rsslink_result = KnownRSS.query.filter_by(rsslink = rsslink).all()
        rsstitle_result = KnownRSS.query.filter_by(rsstitle = rsstitle).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    if len(rsslink_result) != 0:
        return jsonify({'state':'failed', "description": "first query existed with rsslink", "moreMsg":classlist2dictlist(rsslink_result)})
    if len(rsstitle_result) != 0:
        return jsonify({'state':'failed', "description": "first query existed with rsstitle", "moreMsg":classlist2dictlist(rsstitle_result)})

    info = KnownRSS(rsslink, rsstitle)
    try:
        db.session.add(info)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'state':'failed', "description": "second query failed with error: " + str(e.args[0])})

    try:
        result = KnownRSS.query.filter_by(rsslink = rsslink, rsstitle = rsstitle).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    if len(result) == 0:
        return jsonify({'state':'failed', "description": "third query failed with no queryMsg"})
    else:
        return jsonify({"state":'success', "description": "success", "moreMsg":classlist2dictlist(result)})


# 管理员移除一个knownRSS记录
def removeKnownRSS(rssId):
    try:
        result =  KnownRSS.query.filter_by(rssId = rssId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})


# 管理员审核等待队列中的内容记录，包括approved = True为批准通过 和 approved = False为批准未通过
def modifyPendingMsg(administratorId, pendingMsg_id, approved = True):

    try:
        result = pendingMsg.query.filter_by(_Id = pendingMsg_id).all()
        result = [e for e in result if e.checkedByAdministrator == "None"]
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    if len(result) == 0:
        return jsonify({'state':'failed', "description": "first query no existed"})
    result = result[0]

    if approved:
        addKnownRSS_rst = addKnownRSS(result.rsslink, result.rsstitle)
        # if addKnownRSS_rst['state']
        result.checkedByAdministrator = str(administratorId)
        db.session.delete(result)
        db.session.commit()
        return addKnownRSS_rst
    else:
        result.checkedByAdministrator = str(administratorId)
        db.session.delete(result)
        db.session.commit()
        return jsonify({"state":"success", "description": "success"})

# 获取所有knownRSS内容
def getAllRSS():
    try:
        result = KnownRSS.query.all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
