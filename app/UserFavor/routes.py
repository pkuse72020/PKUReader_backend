from app.UserFavor import UserFavor

from flask import request, session, jsonify

from app.tables4favor import FavorRSS, FavorArticle, userAddFavorArticle, userGetFavorArticles, userRemoveFavorArticle ,userGetFavorRSSs, userAddFavorRSS, userRemoveFavorRSS, userGetFavorRSS_links,classlist2dictlist
from app import db

@UserFavor.route('/')
def hello_world():
    return "hello UserFavor!"



@UserFavor.route('/addFavorArticle', methods=["POST", "GET"])
def addUserArticle_func():
    if request.method == "GET":
        userId = request.args.get("userId")
        articleId = request.args.get("articleId")
    else:
        userId = request.form.get("userId")
        articleId = request.form.get("articleId")
    rst = userAddFavorArticle(userId, articleId)
    return rst

@UserFavor.route('/getFavorArticle', methods=["POST", "GET"])
def getUserArticle_func():
    if request.method == "GET":
        userId = request.args.get("userId")
    else:
        userId = request.form.get("userId")
    rst = userGetFavorArticles(userId)
    return rst

@UserFavor.route('/removeFavorArticle', methods=["POST", "GET"])
def removeUserArticle_func():
    if request.method == "GET":
        userId = request.args.get("userId")
        articleId = request.args.get("articleId")
    else:
        userId = request.form.get("userId")
        articleId = request.form.get("articleId")
    rst = userRemoveFavorArticle(userId, articleId)
    return rst

@UserFavor.route('/addFavorRSS', methods=["POST", "GET"])
def addUserRSS_func():
    if request.method == "GET":
        userId = request.args.get("userId")
        RSSId = request.args.get("RSSId")
    else:
        userId = request.form.get("userId")
        RSSId = request.form.get("RSSId")
    rst = userAddFavorRSS(userId, RSSId)
    return rst

@UserFavor.route('/getFavorRSS', methods=["POST", "GET"])
def getUserRSS_func():
    if request.method == "GET":
        userId = request.args.get("userId")
    else:
        userId = request.form.get("userId")
    rst = userGetFavorRSSs(userId)
    return rst

@UserFavor.route('/getFavorRSSlinks', methods=["POST", "GET"])
def getFavorRSSlinks_func():
    if request.method == "GET":
        userId = request.args.get("userId")
    else:
        userId = request.form.get("userId")
    rst = userGetFavorRSS_links(userId)
    return rst

@UserFavor.route('/removeFavorRSS', methods=["POST", "GET"])
def removeUserRSS_func():
    if request.method == "GET":
        userId = request.args.get("userId")
        RSSId = request.args.get("RSSId")
    else:
        userId = request.form.get("userId")
        RSSId = request.form.get("RSSId")
    rst = userRemoveFavorRSS(userId, RSSId)
    return rst


@UserFavor.route('/getAllFavor', methods=["POST", "GET"])
# 测试用
def getAllFavor_debug():
    FavorRSS_result = FavorRSS.query.all()
    FavorArticle_result = FavorArticle.query.all()
    return jsonify({'rss':classlist2dictlist(FavorRSS_result), 'article':classlist2dictlist(FavorArticle_result)})