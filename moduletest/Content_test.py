import unittest
from app import app, db
import json
import base64
from moduletest.encrypt_data import encrypt_data

class ContentTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_articles(self):
        #添加一个用�?        data = {'username': 'yzy', 'password': 'yzyzyyzy'}
        data=encrypt_data(data)
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        userid = response['UserId']
        #添加一个RSS
        data = {'rsslink':'http://39.98.93.128:5001/cctv/tech',
                'rsstitle': 'cctvtech'}
        response = self.client.post("/rssdb/addKnownRSS", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        rssid = str(response['moreMsg'][0]['rssId'])
        #给用户添加一个RSS
        data = {'userId': userid,
                'RSSId': rssid}
        response = self.client.post("/userfavor/addFavorRSS", data=data)
        print(response)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        #生成文章列表
        data = {'userid': userid}
        response = self.client.post("/content/getArticles", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)

    def test_search(self):
        data = {'searchword': "北京"}
        response = self.client.post("/content/search", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)

    def test_get_article_by_id(self):
        # 添加一个用�?        data = {'username': 'lyzy', 'password': 'lyzylzylyzy'}
        data=encrypt_data(data)
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        userid = response['UserId']
        # 添加一个RSS
        data = {'rsslink': 'http://39.98.93.128:5001/cctv/tech',
                'rsstitle': 'cctvtech'}
        response = self.client.post("/rssdb/addKnownRSS", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        rssid = str(response['moreMsg'][0]['rssId'])
        # 给用户添加一个RSS
        data = {'userId': userid,
                'RSSId': rssid}
        response = self.client.post("/userfavor/addFavorRSS", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        # 生成文章列表
        data = {'userid': userid}
        response = self.client.post("/content/getArticles", data=data)
        response = json.loads(response.data)
        articleid = response['article_list']['0']['id']
        self.assertDictContainsSubset({"state": "success"}, response)
        data = {'articleid':articleid}
        response = self.client.post("/content/getArticleById", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)


