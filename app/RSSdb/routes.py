from app.RSSdb import RSSdb

from flask import request, session, jsonify

from app.tables4favor import KnownRSS, pendingMsg, addPendingMsg, getPendingMsg, addKnownRSS, removeKnownRSS, modifyPendingMsg, getAllRSS
from app import db

@RSSdb.route('/')
def hello_world():
    return "hello RSSdb!"

@RSSdb.route('/addPendingMsg', methods=["POST", "GET"])
def addPendingMsg_func():
    if request.method == "GET":
        userId = request.args.get("userId")
        rsstitle = request.args.get("rsstitle")
        rsslink = request.args.get("rsslink")
    else:
        userId = request.form.get("userId")
        rsstitle = request.form.get("rsstitle")
        rsslink = request.form.get("rsslink")
    rst = addPendingMsg(userId, rsstitle, rsslink)
    return rst

@RSSdb.route('/getPendingMsg', methods=["POST", "GET"])
def getPendingMsg_func():
    if request.method == "GET":
        userId = request.args.get("userId")
    else:
        userId = request.form.get("userId")
    rst = getPendingMsg(userId)
    return rst

@RSSdb.route('/addKnownRSS', methods=["POST", "GET"])
def addKnownRSS_func():
    if request.method == "GET":
        rsslink = request.args.get("rsslink")
        rsstitle = request.args.get("rsstitle")
    else:
        rsslink = request.form.get("rsslink")
        rsstitle = request.form.get("rsstitle")
    rst = addKnownRSS(rsslink, rsstitle)
    return rst


@RSSdb.route('/removeKnownRSS', methods=["POST", "GET"])
def removeKnownRSS_func():
    if request.method == "GET":
        rssId = request.args.get("rssId")
    else:
        rssId = request.form.get("rssId")
    rst = removeKnownRSS(rssId)
    return rst

@RSSdb.route('/approvePendingMsg', methods=["POST", "GET"])
def approvePendingMsg_func():
    if request.method == "GET":
        administratorId = request.args.get("administratorId")
        pendingMsg_id = request.args.get("pendingMsg_id")
    else:
        administratorId = request.form.get("administratorId")
        pendingMsg_id = request.form.get("pendingMsg_id")
    rst = modifyPendingMsg(administratorId, pendingMsg_id, approved=True)
    return rst

@RSSdb.route('/rejectPendingMsg', methods=["POST", "GET"])
def rejectPendingMsg_func():
    if request.method == "GET":
        administratorId = request.args.get("administratorId")
        pendingMsg_id = request.args.get("pendingMsg_id")
    else:
        administratorId = request.form.get("administratorId")
        pendingMsg_id = request.form.get("pendingMsg_id")
    rst = modifyPendingMsg(administratorId, pendingMsg_id, approved=False)
    return rst



@RSSdb.route('/getAllRSS')
def getAllRSS_debug():
    return getAllRSS()