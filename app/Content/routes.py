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
    把关键词的wiki内容抽出
    '''
    if request.method == "GET":
        userid = request.args.get("userid")
    else:
        userid = request.form.get("userid")
    #根据username找userid
    try:
        userlist = UserInfo.query.filter_by(UserId=userid).all()
    except Exception as e:
        return jsonify({"state": "failed", "description": e.args[0] + " find user error."})
    if (len(userlist) == 0):
        return jsonify({"state": "failed", "description": "No such user."})
    if (len(userlist) != 1):
        return jsonify({"state": "failed", "description": "There are multiple lines in database with the same Username."})
    user = userlist[0]

    #根据userid找关
    rsslist = []
    try:
        #userfocuslink = UserInfo.query.filter_by(UserId=userid).all()
        userfocuslink = userGetFavorRSS_links_obj(userid)
        #print(userfocuslink)
    except Exception as e:
        return jsonify({"state": "failed", "description": e.args[0] +e.args[1] +  " get favorrss error. "})

    try:
        if userfocuslink['rst'] != None:
            rsslist = [x['rsslink'] for x in userfocuslink['rst']]
        else:
            return jsonify({"state": "failed", "description": "Find no favor RSS"})
    except Exception as e:
        return jsonify({"state": "failed", "description": "Find no favor RSS"})

    article_list = []

    if (len(rsslist) == 0):
        rsslist = ["https://rss.shab.fun/cctv/tech"] #default

    for rssfeed in rsslist:
        entries = feedparser.parse(rssfeed).entries
        if len(entries) > 5:
            entries = entries[:5]
        #print("length of entries: ", len(entries))
        for e in entries:
            cur_title = html2txt(e.title)
            cur_summary = html2txt(e.summary)
            article = Article(cur_title, cur_summary)
            #print(e.title)
            try:
                db.session.add(article)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'state':'failed', 'description':e.args[0]})
            #把文章关键词找出来
            text = cur_summary
            keywordList = getKeywords(text)
            #print(keywordList)
            #关键词入库
            try:
                cur_article = Article.query.filter_by(ArticleTitle=cur_title).all()[0]
            except Exception as e:
                return jsonify({'state':'failed', 'description': 'Save article error.'})
            for word in keywordList:
                cur_a2k = Article2Keyword(cur_article.ArticleId, word)
                try:
                    db.session.add(cur_a2k)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'state':'failed', 'description': e.args[0]})
            keyword_dict = dict(zip(range(len(keywordList)), keywordList))
            newsdata = {'title': cur_article.ArticleTitle, 'article': cur_article.ArticleContent,
                        'id':cur_article.ArticleId, 'keyword_num': len(keywordList), 'keyword_list': keyword_dict}
            es.insert_data(newsdata)
            article_list.append(newsdata)
            index = range(len(article_list))
            article_dict = dict(zip(index, article_list))
    return jsonify({'state': 'success', 'article_list': article_list})

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

    return jsonify({'state': 'success', 'result': es.search_news(searchword)})

@Content.route('/getArticleById', methods=["POST", "GET"])
def get_article_by_id():
    '''
    传入articleid
    :return: Article
    '''
    if request.method == "GET":
        articleid = request.args.get("articleid")
    else:
        articleid = request.form.get("articleid")

    try:
        article_rst = Article.query.filter_by(ArticleId=articleid).all()
    except Exception as e:
        return jsonify({'state':'failed', 'description':'Find Article error'})
    if len(article_rst) == 0:
        return jsonify({'state':'failed', 'description': 'Find No Article.'})
    cur_article = article_rst[0]

    keywordlist = Article2Keyword.query.filter_by(ArticleId=articleid).all()
    keywordlist = [x.Keyword for x in keywordlist]
    keywordlist = dict(zip(range(len(keywordlist)), keywordlist))
    return jsonify({
        'title': cur_article.ArticleTitle,
        'content': cur_article.ArticleContent,
        'keywords': keywordlist
    })

@Content.route('/getallarticle', methods=["POST", "GET"])
def get_all_article():  #仅供测试
    '''
    传入articleid
    :return: Article
    '''
    articlelist = Article.query.all()
    print('debug all article')
    for i, item in enumerate(articlelist):
        print(item.ArticleId)
        print(item.ArticleTitle)
        print(item.ArticleContent)

