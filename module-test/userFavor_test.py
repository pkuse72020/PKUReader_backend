import unittest
from app import app, db
import random
import json
import base64


class UserFavorTestCase(unittest.TestCase):
    user_ids = []
    rsshub_url = 'http://39.98.93.128:5001/'
    rsshub_list = []

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

    def test_1_addAndRemoveRSS(self):
        data = {"username": "gyq", "password": "123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "failed"}, response)

    def test_login(self):
        data = {"username": "gyq", "password": "123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        data = {"username": "gyq", "password": "123456"}
        response = self.client.post("/user/login", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        data = {"username": "gyq123", "password": "123456"}
        response = self.client.post("/user/login", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset(
            {"state": "failed", "description": "No such user."}, response)
        data = {"username": "gyq", "password": "123"}
        response = self.client.post("/user/login", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset(
            {"state": "failed", "description": "Wrong password."}, response)

    def test_token_test(self):
        data = {"username": "gyq", "password": "123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        data = {"username": "gyq", "password": "123456"}
        response = self.client.post("/user/login", data=data)
        response = json.loads(response.data)
        token = response['token']
        headers = {"Authorization": "basic " +
                   base64.b64encode((token + ":").encode("utf-8")).decode("utf-8")}
        response = self.client.post("/user/token_test", headers=headers)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        headers = {"Authorization": "basic " +
                   base64.b64encode((token).encode("utf-8")).decode("utf-8")}
        response = self.client.post("/user/token_test", headers=headers)
        self.assertEqual(response.status_code, 401)
