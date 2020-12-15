import unittest

from flask.wrappers import Response
from requests.api import request
from app import app, db
import random
import json
import base64


class UserFavorTestCase(unittest.TestCase):
    user_ids = []
    rsshub_url = 'http://39.98.93.128:5001/'
    rsshub_list = [('央视新闻 tech', 'http://39.98.93.128:5001/cctv/tech'),('AI研习社', 'http://39.98.93.128:5001/aiyanxishe/all')]
    user_name = 'test_user1'
    article_id = [1,2]
    # rss_id = [1,2]

    @classmethod
    def setUpClass(cls):
        print("start test UserFavor...")
        app.testing = True
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        print("end test UserFavor...")
        db.session.remove()
        db.drop_all()

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def getUserArticle(self, len_num):
        data = {'userId':UserFavorTestCase.user_name}
        response = self.client.post("/userfavor/getFavorArticle",data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allArticle_len = len(response['rst'])
        self.assertEqual(len_num, allArticle_len)

    def test_1_addAndRemoveRSS(self):
        for e in UserFavorTestCase.article_id:
            data = {'userId':UserFavorTestCase.user_name, 'articleId': e}
            response = self.client.post("/userfavor/addFavorArticle", data = data)
            response = json.loads(response.data)
        self.getUserArticle(2)

        data = {'userId':UserFavorTestCase.user_name, 'articleId': 1}
        response = self.client.post("/userfavor/removeFavorArticle", data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)

        self.getUserArticle(1)

        data = {'userId':UserFavorTestCase.user_name, 'articleId': 1}
        response = self.client.post("/userfavor/removeFavorArticle", data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"failed"}, response)

        self.getUserArticle(1)


    
    def test_2_addRSS(self):
        for e in UserFavorTestCase.rsshub_list:
            data = {'rsslink':e[1],'rsstitle':e[0]}
            response = self.client.post("/rssdb/addKnownRSS",data = data)
            response = json.loads(response.data)
            self.assertDictContainsSubset({"state":"success"}, response)

    def getUserRSS(self, len_num):
        data = {'userId':UserFavorTestCase.user_name}
        response = self.client.post("/userfavor/getFavorRSS",data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allArticle_len = len(response['rst'])
        self.assertEqual(len_num, allArticle_len)

    def test_3_addAndRemoveArticle(self):
        response = self.client.post("/rssdb/getAllRSS")
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allRSSs = response['rst']
        allRSS_ids = [e['rssId'] for e in allRSSs]
        for e in allRSS_ids:
            data = {'userId':UserFavorTestCase.user_name, "RSSId":e}
            response = self.client.post("/userfavor/addFavorRSS",data = data)
            response = json.loads(response.data)
            self.assertDictContainsSubset({"state":"success"}, response)
        self.getUserRSS(len(allRSS_ids))

        self.assertEqual(len(allRSS_ids), len(UserFavorTestCase.rsshub_list))

        # test get rsslinks
        data = {'userId':UserFavorTestCase.user_name}
        response = self.client.post("/userfavor/getFavorRSSlinks",data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allRSS_len = len(response['rst'])
        self.assertEqual(len(allRSS_ids), allRSS_len)

        # test remove rsslinks
        data = {'userId':UserFavorTestCase.user_name, "RSSId":allRSS_ids[0]}
        response = self.client.post("/userfavor/removeFavorRSS",data = data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        self.getUserRSS(len(allRSS_ids) - 1)
        




