import unittest
from app import app,db
import random,json,base64

class UserManagementTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        # db.drop_all()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # db.create_all()

    def test_signup(self):
        data = {"username":"gyq","password":"123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"},response)
        response = self.client.post("/user/signup",data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "failed"}, response)
        
    def test_login(self):
        data = {"username":"gyq","password":"123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"},response)
        data = {"username":"gyq","password":"123456"}
        response = self.client.post("/user/login",data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"}, response)
        data = {"username":"gyq123","password":"123456"}
        response = self.client.post("/user/login",data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "failed", "description": "No such user."}, response)
        data = {"username":"gyq","password":"123"}
        response = self.client.post("/user/login",data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "failed", "description": "Wrong password."}, response)
        
    def test_token_test(self):
        data = {"username":"gyq","password":"123456"}
        response = self.client.post("/user/signup", data=data)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"},response)
        data = {"username":"gyq","password":"123456"}
        response = self.client.post("/user/login",data=data)
        response = json.loads(response.data)
        token=response['token']
        headers = {"Authorization": "basic " + base64.b64encode((token + ":").encode("utf-8")).decode("utf-8")}
        response = self.client.post("/user/token_test", headers=headers)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.data)
        self.assertDictContainsSubset({"state": "success"},response)
        