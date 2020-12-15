# UserFavor 模块说明

> 测试代码见`userFavor测试 代码.ipynb`

### getAllFavor

- 获取favorRSS和favorArticle，为测试用接口，实际生产需要注释掉

- ```python
  data = {}
  response = requests.post("http://127.0.0.1:5000/userfavor/getAllFavor",data=data)
  response.json()
  ```

- ```
  {'article': [{'_Id': 2, 'articleId': 997, 'userId': 'test_user1'},
    {'_Id': 3, 'articleId': 997, 'userId': 'test_user2'},
    {'_Id': 4, 'articleId': 996, 'userId': 'test_user1'}],
   'rss': [{'_Id': 1, 'rssId': 12, 'userId': 'test_user1'},
    {'_Id': 2, 'rssId': 11, 'userId': 'test_user1'},
    {'_Id': 3, 'rssId': 11, 'userId': 'test_user2'}]}
  ```

### addFavorArticle

- 为指定用户增加一个收藏文章

- ```python
  data = {'userId':'test_user1','articleId':'996'}
  response = requests.post("http://127.0.0.1:5000/userfavor/addFavorArticle",data=data)
  response.json()
  ```

- ```
  {'description': 'success',
   'moreMsg': [{'_Id': 4, 'articleId': 996, 'userId': 'test_user1'}],
   'state': 'success'}
  ```



### getFavorArticle

- 为指定用户获取其全部收藏文章

- ```python
  data = {'userId':'test_user1'}
  response = requests.post("http://127.0.0.1:5000/userfavor/getFavorArticle",data=data)
  response.json()
  ```

- ```
  {'rst': [{'_Id': 2, 'articleId': 997, 'userId': 'test_user1'},
    {'_Id': 4, 'articleId': 996, 'userId': 'test_user1'}],
   'state': 'success'}
  ```
  
  
  

  
### removeFavorArticle

- 为指定用户删除一篇收藏文章

- ```python
  data = {'userId':'test_user1','articleId':'996'}
  response = requests.post("http://127.0.0.1:5000/userfavor/removeFavorArticle",data=data)
  response.json()
  ```

- ```
  {'description': "third query failed with errors: Class 'builtins.NoneType' is not mapped",
   'state': 'failed'}
  ```





### addFavorRSS

- 为指定用户订阅一个RSS

- ```python
  data = {'userId':'test_user2','RSSId':'15'}
  response = requests.post("http://127.0.0.1:5000/userfavor/addFavorRSS",data=data)
  response.json()
  ```

- ```
  {'description': 'success',
   'moreMsg': [{'_Id': 5, 'rssId': 15, 'userId': 'test_user2'}],
   'state': 'success'}
  ```





### getFavorRSS

- 为指定用户获取订阅的所有RSS_id

- ```python
  data = {'userId':'test_user2'}
  response = requests.post("http://127.0.0.1:5000/userfavor/getFavorRSS",data=data)
  response.json()
  ```

- ```
  {'rst': [{'_Id': 3, 'rssId': 11, 'userId': 'test_user2'},
    {'_Id': 4, 'rssId': 13, 'userId': 'test_user2'},
    {'_Id': 5, 'rssId': 15, 'userId': 'test_user2'}],
   'state': 'success'}
  ```



### userGetFavorRSS_links

- 为指定用户获取订阅的所有RSS_title和rss_link

- ```python
  data = {'userId':'test_user2'}
  response = requests.post("http://127.0.0.1:5000/userfavor/getFavorRSSlinks",data=data)
  response.json()
  ```

- ```
  {'rst': [{'_Id': 3,
     'rsslink': 'www.bilibili.com9',
     'rsstitle': 'bilibili9',
     'userId': 'test_user2'},
    {'_Id': 4,
     'rsslink': 'www.bilibili.com11',
     'rsstitle': 'bilibili11',
     'userId': 'test_user2'},
    {'_Id': 5,
     'rsslink': 'www.bilibili.com13',
     'rsstitle': 'bilibili13',
     'userId': 'test_user2'}],
   'state': 'success'}
  ```



### removeFavorRSS

- 为指定用户移除一个RSS订阅

- ```python
  data = {'userId':'test_user1','RSSId':'11'}
  response = requests.post("http://127.0.0.1:5000/userfavor/removeFavorRSS",data=data)
  response.json()
  ```

- ```
  {'description': "third query failed with errors: Class 'builtins.NoneType' is not mapped",
   'state': 'failed'}
  ```

