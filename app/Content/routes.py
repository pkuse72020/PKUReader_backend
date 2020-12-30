from typing import DefaultDict
from app.Content import Content
from flask import request, session, jsonify
import feedparser
import sqlite3
import re
from langconv import *

@Content.route('/')
def hello_world():
    return "content helloworld!"

from app import db, es, WIKI_DIR
from app.tables import *
from app.tables4favor import *
from NLProcess.tools import html2txt, html2txt_yzy, tokenizer, getEachPOS, getKeywords

def showenter(text):
    ret = text.replace("<br>", '\n')
    ret = ret.replace("<p></p>", '\n')
    return ret

def getImgLink(text):
    DEFAULT_IMG = ['https://cn.bing.com/th?id=OHR.IbonPlan_ZH-CN8564017247_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.BarnettsDemesne_ZH-CN8484261440_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.FRbluebirds_ZH-CN3972483010_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.WildReindeer_ZH-CN8301029606_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.BandedPipefish_ZH-CN8209616080_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.HolidayNubble_ZH-CN8122183595_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
    'https://cn.bing.com/th?id=OHR.CastleriggStone_ZH-CN8015482045_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp']
    pattern1 = re.compile(r'<img(.*?)/>')
    pattern2 = re.compile(r'src="(.*?)"')
    first_rst = pattern1.findall(text)
    second_rst = [pattern2.findall(e) for e in first_rst]
    second_rst = [e for ee in second_rst for e in ee]
    # second_rst += DEFAULT_IMG
    if len(second_rst) == 0:
        second_rst = DEFAULT_IMG
    return second_rst


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
            #cur_summary = html2txt(e.summary)
            cur_summary = e.summary
            article = Article(cur_title, cur_summary)
            #print(e.title)
            findarticle = Article.query.filter_by(ArticleTitle=cur_title).all()
            if len(findarticle) != 0:
                cur_article = findarticle[0]
                articleid = cur_article.ArticleId
                keywordList = Article2Keyword.query.filter_by(ArticleId=articleid).all()
                keywordList = [x.Keyword for x in keywordList]
                keyword_dict = dict(zip(range(len(keywordList)), keywordList))
                raw_content = cur_article.ArticleContent
                raw_html = raw_content
                imgLinks_list = getImgLink(raw_content)
                raw_content = showenter(raw_content)
                show_content = html2txt_yzy(raw_content)
                newsdata = {'title': cur_article.ArticleTitle, 'article': show_content,
                            'id': cur_article.ArticleId, 'keyword_num': len(keywordList), 'keyword_list': keyword_dict,'imgLinks': imgLinks_list, 
                            'raw_html':raw_html}
                article_list.append(newsdata)
            else:
                try:
                    db.session.add(article)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'state':'failed', 'description':e.args[0]})
                #把文章关键词找出来
                text = html2txt(cur_summary)
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
                raw_content = cur_article.ArticleContent
                raw_html = raw_content
                imgLinks_list = getImgLink(raw_content)
                raw_content = showenter(raw_content)
                show_content = html2txt_yzy(raw_content)
                newsdata = {'title': cur_article.ArticleTitle, 'article': show_content,
                            'id':cur_article.ArticleId, 'keyword_num': len(keywordList), 'keyword_list': keyword_dict, 'imgLinks': imgLinks_list, 
                            'raw_html':raw_html}
                es.insert_data(newsdata)
                article_list.append(newsdata)
    index = range(len(article_list))
    article_dict = dict(zip(index, article_list))
    return jsonify({'state': 'success', 'article_list': article_dict})

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

    try:
        res = es.search_news(searchword)
        res = json.loads(res)
        article_list = []
        for item in res['hits']['hits']:
            article_list.append(item["_source"])
        article_dict = dict(zip(range(len(article_list)), article_list))
    except Exception as e:
        return jsonify({'state':'failed',
                        'description': 'Search Error.'})
    return jsonify({'state': 'success', 'result': article_dict})


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
        return_dict = getArticleByID(articleid)
    except Exception as e:
        return jsonify({'state':'failed', 'description':'Find Article error'})

    if return_dict == None:
        return jsonify({'state':'failed', 'description': 'Find No Article.'})
    return jsonify(return_dict)

    # try:
    #     article_rst = Article.query.filter_by(ArticleId=articleid).all()
    # except Exception as e:
    #     return jsonify({'state':'failed', 'description':'Find Article error'})
    # if len(article_rst) == 0:
    #     return jsonify({'state':'failed', 'description': 'Find No Article.'})
    # cur_article = article_rst[0]

    # keywordlist = Article2Keyword.query.filter_by(ArticleId=articleid).all()
    # keywordlist = [x.Keyword for x in keywordlist]
    # keywordlist = dict(zip(range(len(keywordlist)), keywordlist))
    # return jsonify({
    #     'title': cur_article.ArticleTitle,
    #     'article ': cur_article.ArticleContent,
    #     'keywords': keywordlist,
    #     'state': 'success'
    # })

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

@Content.route('/getWiki', methods=["POST", "GET"])
def serchword():
    if request.method == "GET":
        wikiword = request.args.get("wikiword")
    else:
        wikiword = request.form.get("wikiword")
    t = list(wikiword)
    if(ord(t[0])>96 and ord(t[0])<123):
        p=ord(t[0])-32
        t[0]=chr(p)
        wikiword = ''.join(t)
    con_wikidb = sqlite3.connect(WIKI_DIR)
    cursor = con_wikidb.cursor()#数据库连接
    def cht_to_chs(line):
        line = Converter('zh-hans').convert(line)
        line.encode('utf-8')
        return line
    try:
        sql = "select * from review1 where Article_title = "+"'"+wikiword+"'"#查询操作
        cursor.execute(sql)
        result = cursor.fetchall()
    except Exception as e:
        con_wikidb.rollback()
        return jsonify({"state":"failed", "description":e.args[0]})
    
    if(str(result) == "[]" ):
        sql3 = "select * from redirectindex where title = "+"'"+wikiword+"'"
        cursor.execute(sql3)
        index = cursor.fetchall()
        lenth = len(index)
        flag = 0
        for i in range(lenth):
            index1 = index[i][0]
            sql4 = "select * from redirect where rd_from = "+"'"+index1+"'"
            cursor.execute(sql4)
            result4 = cursor.fetchall()
            if(str(result4) == "[]" ):
                continue
            else:
                t2 = cht_to_chs(result4[0][2])
                sql5 = "select * from review1 where Article_title = "+"'"+t2+"'"
                cursor.execute(sql5)
                result5 = cursor.fetchall()
                flag = 1
                break
        if(flag == 1):
            s3 = result5
            return jsonify({"state":"success", "result":s3})
        else:
            s = result
            return jsonify({"state":"success", "result":s})
    else:
        s = result
        return jsonify({"state":"success", "result":s})
    cursor.close()
    con_wikidb.close()



