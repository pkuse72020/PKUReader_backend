import unittest
from app import app, db
import random
import json
import base64


class RSSDBTestCase(unittest.TestCase):
    user_ids = []
    rsshub_url = 'http://39.98.93.128:5001/'
    rsshub_list = [('央视新闻 tech', 'http://39.98.93.128:5001/cctv/tech'),('AI研习社', 'http://39.98.93.128:5001/aiyanxishe/all')]
    # pendingMsg的长度需要为2，用于处理请求同意失败各一个
    pendingMsg = [('X玖少年团肖战DAYTOY的微博', 'http://39.98.93.128:5001/weibo/user/1792951112'), ('邓香兰的微博', 'http://39.98.93.128:5001/weibo/user/6054858390')]

    user_id = 'test_user'
    administrator_name = 'test_administrator'

    @classmethod
    def setUpClass(cls):
        print("start test RSSDB...")
        app.testing = True
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        print("end test RSSDB...")
        db.session.remove()
        db.drop_all()

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def tearDown(self):
        pass

    def test_1_addAndRemoveRSS(self):
        for e in RSSDBTestCase.rsshub_list:
            data = {'rsslink':e[1],'rsstitle':e[0]}
            response = self.client.post("/rssdb/addKnownRSS",data = data)
            response = json.load(response.data)
            self.assertDictContainsSubset({"state":"success"}, response)
    def test_2_getAllRSS(self):
        response = self.client.post("/rssdb/getAllRSS")
        response = json.load(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allRSS_len = len(response['rst'])
        self.assertEqual(len(RSSDBTestCase.rsshub_list), allRSS_len)

    def test_3_addPendingMsg(self):
        # 添加已有的内容必然会失败
        for e in RSSDBTestCase.rsshub_list:
            data = {'userId':'test_user1','rsslink':e[1],'rsstitle':e[0]}
            response = self.client.post("/rssdb/addPendingMsg",data = data)
            response = json.load(response.data)
            self.assertDictContainsSubset({'state': 'failed'}, response)
        for e in RSSDBTestCase.pendingMsg:
            data = {'userId':'test_user1','rsslink':e[1],'rsstitle':e[0]}
            response = self.client.post("/rssdb/addPendingMsg",data = data)
            response = json.load(response.data)
            self.assertDictContainsSubset({'state': 'success'}, response)

    def test_4_handlePendingMsg(self):
        response = self.client.post("/rssdb/getPendingMsg")
        pending_response = json.load(response.data)
        self.assertDictContainsSubset({"state":"success"}, pending_response)
        pendingMsg_len = len(pending_response['rst'])
        self.assertEqual(len(RSSDBTestCase.pendingMsg),pendingMsg_len)

        # 同意第一个请求
        approve_id = pending_response['rst'][0]['_Id']
        data = {'administratorId':RSSDBTestCase.administrator_name,'pendingMsg_id':approve_id}
        response = self.client.post("/rssdb/approvePendingMsg")
        response = json.load(response.data)
        self.assertDictContainsSubset({'state': 'success'}, response)

        # 再次查看所有RSS，数量应该+1
        response = self.client.post("/rssdb/getAllRSS")
        response = json.load(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allRSS_len = len(response['rst'])
        self.assertEqual(len(RSSDBTestCase.rsshub_list) + 1, allRSS_len)

        
        # 拒绝第二个请求
        reject_id = pending_response['rst'][1]['_Id']
        data = {'administratorId':RSSDBTestCase.administrator_name,'pendingMsg_id':approve_id}
        response = self.client.post("/rssdb/rejectPendingMsg")
        response = json.load(response.data)
        self.assertDictContainsSubset({'state': 'success'}, response)

        response = self.client.post("/rssdb/getAllRSS")
        response = json.load(response.data)
        self.assertDictContainsSubset({"state":"success"}, response)
        allRSS_len = len(response['rst'])
        self.assertEqual(len(RSSDBTestCase.rsshub_list) + 1, allRSS_len)

    def test_5_getPendingMsg(self):
        # 处理完所有之后应该为0
        response = self.client.post("/rssdb/getPendingMsg")
        pending_response = json.load(response.data)
        self.assertDictContainsSubset({"state":"success"}, pending_response)
        pendingMsg_len = len(pending_response['rst'])
        self.assertEqual(0,pendingMsg_len)

