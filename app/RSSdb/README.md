# rssdb模块说明

> 测试代码见`rssdb测试 代码.ipynb`

### getPendingMsg

- 获取所有请求队列

- ```python
  response = requests.post("http://127.0.0.1:5000/rssdb/getPendingMsg")
  response.json()
  ```
  
- ```
  {'rst': [{'_Id': 8,
     'checkedByAdministrator': 'None',
     'rsslink': 'www.baidu.com',
     'rsstitle': 'baidu',
     'userId': 'test_user'},
    {'_Id': 9,
     'checkedByAdministrator': 'None',
     'rsslink': 'www.baidu.com',
     'rsstitle': 'baidu',
     'userId': 'test_user'},
    {'_Id': 10,
     'checkedByAdministrator': 'None',
     'rsslink': 'www.baidu.com',
     'rsstitle': 'baidu',
     'userId': 'test_user'},
    {'_Id': 11,
     'checkedByAdministrator': 'None',
     'rsslink': 'www.baid1u.com',
     'rsstitle': 'baidu1',
     'userId': 'test_user1'}],
   'state': 'success'}
  ```

### addPendingMsg

- 在等待队列中增加一个请求

- ```python
  data = {'userId':'test_user1','rsstitle':'baidu1','rsslink':'www.baid1u.com'}
  response = requests.post("http://127.0.0.1:5000/rssdb/addPendingMsg",data=data)
  response.json()
  ```

- ```
  {'description': 'success',
   'moreMsg': [{'_Id': 11,
     'checkedByAdministrator': 'None',
     'rsslink': 'www.baid1u.com',
     'rsstitle': 'baidu1',
     'userId': 'test_user1'}],
   'state': 'success'}
  ```



### approvePendingMsg

- 管理员同意队列中的一个请求，并将该请求放入knownRSS数据库中

- ```python
  data = {'administratorId':'test_admin','pendingMsg_id':11}
  response = requests.post("http://127.0.0.1:5000/rssdb/approvePendingMsg",data=data)
  response.json()
  ```

- ```
  {'description': 'success',
   'moreMsg': [{'rssId': 2, 'rsslink': 'www.baid1u.com', 'rsstitle': 'baidu1'}],
   'state': 'success'}
  ```
  
  
  

  
### rejectPendingMsg

- 管理员拒绝一个请求

- ```python
  data = {'administratorId':'test_admin','pendingMsg_id':7}
  response = requests.post("http://127.0.0.1:5000/rssdb/rejectPendingMsg",data=data)
  response.json()
  ```

- ```
  {'description': 'first query no existed', 'state': 'failed'}
  ```





### getAllRSS

- 获取所有knownRSS内容

- ```python
  data = {}
  response = requests.post("http://127.0.0.1:5000/rssdb/getAllRSS")
  response.json()
  ```

- ```
  {'rst': [{'rssId': 1, 'rsslink': 'www.baidu.com', 'rsstitle': 'baidu'}],
   'state': 'success'}
  ```





### addKnownRSS

- 直接在knownRSS中增加一个内容，跳过pendingMsg管理员审核

- ```python
  data = {'rsslink':'www.bilibili.com','rsstitle':'bilibili'}
  response = requests.post("http://127.0.0.1:5000/rssdb/addKnownRSS",data=data)
  response.json()
  ```

- ```
  {'description': 'success',
   'moreMsg': [{'rssId': 2,
     'rsslink': 'www.bilibili.com',
     'rsstitle': 'bilibili'}],
   'state': 'success'}
  ```



### removeKnownRSS

- 在knownRSS中删除一个内容

- ```python
  data = {'rssId':2}
  response = requests.post("http://127.0.0.1:5000/rssdb/removeKnownRSS",data=data)
  response.json()
  ```

- ```
  {'description': 'success', 'state': 'success'}
  ```


