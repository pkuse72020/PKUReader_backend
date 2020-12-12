from flask import json
from flask.json import jsonify
from app import db
import uuid

import app

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
    articleId = db.Column(db.Integer, nullable=False)

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


def userGetFavorArticles(userId):
    try:
        result = FavorArticle.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
    # return [{'_Id':e._Id,'userId':e.userId, "articleId":e.articleId} for e in result]

def userRemoveFavorArticle(userId, articleId):
    try:
        result = FavorArticle.query.filter_by(userId = userId, articleId = articleId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})

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

def userGetFavorRSSs(userId):
    try:
        result = FavorRSS.query.filter_by(userId = userId).all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
    # return [{'_Id':e._Id,'userId':e.userId, "rssId":e.rssId} for e in result]

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
        rst = [{'_Id':e['_Id'], 'userId':e['userId'], 'rsslink':rssid2rsslink[e['rssId']],'rsstitle':rssid2rsstitle[e['rssId']]} for e in rst]
        return jsonify({'state':'success', "rst":rst})
    except Exception as e:
        return jsonify({'state':'failed', "description": str(e.args[0])})



def userRemoveFavorRSS(userId, RSSId):
    try:
        result =  FavorRSS.query.filter_by(userId = userId, rssId = RSSId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})

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

def getPendingMsg(administratorId):
    try:
        result = pendingMsg.query.filter(pendingMsg.checkedByAdministrator == "None").all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})

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


def removeKnownRSS(rssId):
    try:
        result =  KnownRSS.query.filter_by(rssId = rssId).first()
        db.session.delete(result)
        db.session.commit()
    except Exception as e:
        return jsonify({'state':'failed', "description": "third query failed with errors: " + str(e.args[0])})
    else:
        return jsonify({"state":'success', "description": "success"})

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

def getAllRSS():
    try:
        result = KnownRSS.query.all()
    except Exception as e:
        return jsonify({'state':'failed', "description": "first query failed with error: " + str(e.args[0])})
    return jsonify({'state':'success', "rst":classlist2dictlist(result)})
