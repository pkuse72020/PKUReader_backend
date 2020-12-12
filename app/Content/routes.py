from app.Content import Content
from flask import request, session, jsonify
import feedparser

@Content.route('/')
def hello_world():
    return "content helloworld!"

from app import db, es
from app.tables import *
from app.tables4favor import *
from NLProcess.tools import html2txt, tokenizer, getEachPOS, getKeywords

@Content.route('/getArticles', methods=["POST", "GET"])
def get_articles():
    '''
    传入用户名；
    返回推送给用户的文章列表；
    给文章生成关键词，并放入数据库；
    把关键词的wiki内容抽出；
    '''
    if request.method == "GET":
        username = request.args.get("username")
    else:
        username = request.form.get("username")
    #根据username找userid
    try:
        userlist = UserInfo.query.filter_by(Username=username).all()
    except Exception as e:
        return jsonify({"state": "failed", "description": e.args[0]})
    if (len(userlist) == 0):
        return jsonify({"state": "failed", "description": "No such user."})
    if (len(userlist) != 1):
        return jsonify({"state": "failed", "description": "There are multiple lines in database with the same Username."})
    user = userlist[0]
    userid = user.UserId

    #根据userid找关注
    try:
        #userfocuslink = UserInfo.query.filter_by(UserId=userid).all()
        userfocuslink = userGetFavorRSS_links_obj(userid)
        rsslist = [e['rsslink'] for e in userfocuslink]
    #rst = [{'_Id': e['_Id'], 'userId': e['userId'], 'rsslink': rssid2rsslink[e['rssId']],
    #        'rsstitle': rssid2rsstitle[e['rssId']]} for e in rst]
    except Exception as e:
        return jsonify({"state": "failed", "description": e.args[0]})

    article_list = []

    if (len(rsslist) == 0):
        rsslist = ["https://rsshub.app/aiyanxishe/109/hot", "https://rsshub.app/005tv/zx/latest"]

    for rssfeed in rsslist:
        entries = feedparser.parse(rssfeed).entries
        if len(entries) > 5:
            entries = entries[:5]
        for e in entries:
            article = Article(e.title, e.summary)
            db.session.add(article)
            #把文章关键词找出来
            text = html2txt(e.summary)
            keywordList = getKeywords(text)
            #关键词入库
            cur_article = db.session.query.filter_by(ArticleTitle=e.title).all()[0]
            #TODO 需要检查
            for word in keywordList:
                cur_a2k = Article2Keyword(cur_article.ArticleId, word)
                db.session.add(cur_a2k)

            newsdata = {'title': cur_article.ArticleTitle, 'article': cur_article.ArticleContent,
                        'id':cur_article.ArticleId}
            es.insert_data(newsdata)
            article_list.append(jsonify(newsdata)) #TODO wiki内容

    return article_list

@Content.route('/search', methods=["POST", "GET"])
def search():
    '''
    传入关键词；
    返回一个相关文章列表；
    '''
    #searchword = "的 是 中国"
    if request.method == "GET":
        searchword = request.args.get("searchword")
    else:
        searchword = request.form.get("searchword")

    print(es.search_news(searchword))
