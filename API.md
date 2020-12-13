 # API文档

<!-- TOC -->

- [API文档](#api文档)
  - [**UserManagement**](#usermanagement)
    - [token的使用方式](#token的使用方式)
    - [/user/signup](#usersignup)
    - [/user/login](#userlogin)
    - [/user/token_test](#usertoken_test)

<!-- /TOC -->

[TOC]

## UserManagement
此模块主要用于进行用户的登录、注册、以及token的验证工作

**现阶段用户名以及密码传输均采用明文传输，后续会考虑使用rsa加密传输**

### token的使用方式

拿到token后，使用方法为在http请求的header中添加一项(此方法手动构建header，可以考虑其他方法)
```
{
    "Authorization": "basic "+ base64(token+":") # 注意basic后有一个空格，token后面需要添加一个冒号再做base64加密
}
```
如果token验证通过，服务器返回
```
{
    state: "success"
}
```
否则，服务器会返回状态码401(UNAUTHORIZED)，表明失效

对于后端任意函数，如果要求只有登录状态才能使用，须在函数定义前加
```
@auth.login_required
def example():
    # do something
```
这样就会自动使用上述token验证机制



### /user/signup
此路径用于进行用户注册

支持Get方法和Post方法

输入：
```
{
    username: String, # 用户名
    password: String  # 密码
}
```

输出：

成功时：
```
{
    state: "success"
}
```

失败时：
```
{
    state: "failed",
    description: String # 给出一个错误原因
}
```


### /user/login
此路径用于进行用户登录

支持Get方法和Post方法

输入：
```
{
    username: String, # 用户名
    password: String  # 密码
}
```

输出：

成功时：
```
{
    state: "success",
    UserId: String, # 用户ID，请务必在本地保存，后续需要使用
    token: String # 后续操作使用的token
}
```

失败时：
```
{
    state: "failed",
    description: String # 给出一个错误原因
}
```

### /user/token_test
用于验证token是否还有效。如果token无效需要重新登录获取token



## UserFavor

> 用于用户收藏文章、用户订阅新RSS链接

### /userfavor/addFavorArticle

> 用户添加收藏文章

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
      'articleId':'1' // 文章id，用字符串表示数字，用于唯一确定文章，对应文章数据库中的id
  }
  ```

- 输出：

  - 成功时：

      ```json
      {
          'state': 'success', //成功状态
          'moreMsg': [{'_Id': 1, 'articleId': 1, 'userId': 'test_user1'}], // 表示该添加内容在数据库中的项
          'description': 'success', // 成功描述
      } 
    ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  

### /userfavor/getFavorArticle

> 用户获取已收藏的文章

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1, 'articleId': 996, 'userId': 'test_user1'}], // 列表，每一项表示一条数据库记录
          'state': 'success' // 成功状态
      }
      ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  

### /userfavor/removeFavorArticle

> 用户移除一篇收藏文章

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
      'articleId':'1' // 文章id，用字符串表示数字，用于唯一确定文章，对应文章数据库中的id
  }
  ```

- 输出：

  - 成功时：

      ```json
      {
          'state': 'success', //成功状态
          'description': 'success', // 成功描述
      } 
      ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  



### /userfavor/addFavorRSS

> 用户订阅一个新RSS

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
      'RSSId':'1' // RSSid，用字符串表示数字，用于唯一确定RSS，对应RSS数据库中的id
  }
  ```

- 输出：

  - 成功时：

      ```json
      {
          'state': 'success', //成功状态
          'moreMsg': [{'_Id': 9, 'rssId': 1, 'userId': 'test_user1'}], // 表示该添加内容在数据库中的项
          'description': 'success', // 成功描述
      } 
    ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  

### /userfavor/getFavorRSS

> 用户获取所有已订阅的RSS链接的id

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1, 'rssId': 1, 'userId': 'test_user1'},
                  {'_Id': 2, 'rssId': 2, 'userId': 'test_user1'},
                  {'_Id': 3, 'rssId': 5, 'userId': 'test_user1'},
                  {'_Id': 4, 'rssId': 6, 'userId': 'test_user1'},
                {'_Id': 5, 'rssId': 7, 'userId': 'test_user1'},
                {'_Id': 6, 'rssId': 10, 'userId': 'test_user1'}], // 数据库内容
        'state': 'success' // 成功状态
    }
    ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  

### /userfavor/getFavorRSSlinks

> 用户获取所有已订阅的RSS的标题和链接

- 输入：

  ```json
  {
      'userId':'test_user1', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1,
                   'rsslink': 'https://rss.injahow.cn/zhihu/people/activities/li-xi-mo-66',
                   'rsstitle': 'liximo66的知乎',
                   'userId': 'test_user1'},
                  {'_Id': 2,
                   'rsslink': 'https://rss.injahow.cn/zhihu/hotlist',
                   'rsstitle': '知乎热搜',
                 'userId': 'test_user1'}
                ], // 数据库内记录
        'state': 'success' // 成功状态
    }
    ```
    
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  

### /userfavor/removeFavorRSS

> 用户取消订阅一个RSS

- 输入：

  ```json
  {
      'userId':'test_user1', // 用户标识符
      'RSSId':'11' // RSS标识符
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success', 
          'state': 'success'
      }  
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  





## rssdb

> 用于维护已公布的RSSlink数据库和用户提交请求数据库

### /rssdb/getPendingMsg

> 管理员 获取所有用户已经提交的但尚未处理的申请

- 输入：

  ```json
  None
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [
             	 	{'_Id': 1, // 该申请的id
                   'checkedByAdministrator': 'None', // 该项表示该记录被哪个管理员处理了，在该api中全为None
                   'rsslink': 'www.baid1u.com',
                   'rsstitle': 'baidu1',
                   'userId': 'test_user1'}
          		], // 列表，每一项表示一个未处理的请求
          'state': 'success'}
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  


### /rssdb/addPendingMsg

> 用户提交一个新的RSS申请

- 输入：

  ```json
  {
      'userId':'test_user1', // 用户标识符
      'rsstitle':'baidu', // 新的RSS申请的标题
      'rsslink':'www.baidu.com' // 新的RSS申请的链接
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success', // 成功描述
          'moreMsg': [{'_Id': 1,
                       'checkedByAdministrator': 'None',
                       'rsslink': 'www.baid1u.com',
                       'rsstitle': 'baidu1', 
                       'userId': 'test_user1'}], // 该申请在数据库中的项的具体信息
          'state': 'success' // 成功状态
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
      
      - 其中有两种错误需要特殊处理：
      
      - ```json
          // 表示已有的knownRSS数据库中已经有相同rsslink的记录了
          {
              'state':'failed', "description": "first query existed with rsslink"
          }
          
          // 表示已有的knownRSS数据库中已经有相同的rsstitle的记录了
          {
              'state':'failed', "description": "first query existed with rsstitle"
          }
          ```
  



### /rssdb/approvePendingMsg

> 管理员 批准通过某条申请

- 输入：

  ```json
  {
      'administratorId':'test_admin', // 管理员id
      'pendingMsg_id':11 // 该申请的id
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success', // 成功描述
          'moreMsg': [{'rssId': 20,
                       'rsslink': 'http://news.baidu.com/n?cmd=1&class=civilnews&tn=rss',
                    	'rsstitle': 'baidu'}], //该项在knownRSS数据库中的具体项信息
          'state': 'success' // 成功状态
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  
      
      - 其中有两种错误需要特殊处理：
      
      - ```json
          // 表示已有的knownRSS数据库中已经有相同rsslink的记录了
          {
              'state':'failed', "description": "first query existed with rsslink"
          }
          
          // 表示已有的knownRSS数据库中已经有相同的rsstitle的记录了
          {
              'state':'failed', "description": "first query existed with rsstitle"
          }
          ```
  



### /rssdb/rejectPendingMsg

> 管理员 拒绝某个申请

- 输入：

  ```json
  {
      'administratorId':'test_admin', // 管理员id
      'pendingMsg_id':11 // 该申请的id
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success', 
          'state': 'success'
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  



### /rssdb/getAllRSS

> 获取所有预制已保存的knownRSS

- 输入：

  ```json
  None
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'rssId': 1,
                   'rsslink': 'https://rss.injahow.cn/zhihu/people/activities/li-xi-mo-66',
                   'rsstitle': 'liximo66的知乎'},
                  {'rssId': 2,
                   'rsslink': 'https://rss.injahow.cn/zhihu/hotlist',
                   'rsstitle': '知乎热榜'}],
          'state': 'success'
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  




### /rssdb/addKnownRSS

> 注意：该api用于debug！！！
>
> 管理员 直接添加一个新的RSS

- 输入：

  ```json
  {
      'rsslink':"https://rss.injahow.cn/zhihu/people/activities/li-xi-mo-66", // rss链接
      'rsstitle':"知乎liximo66" // rss标题
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success',  //成功描述
          'moreMsg': [{'rssId': 1, 
                       'rsslink': 'https://rss.injahow.cn/zhihu/people/activities/li-xi-mo-66', 
                       'rsstitle': 'zhihu/people/activities/li-xi-mo-66'}],  // 在数据库中的具体信息
          'state': 'success' // 成功状态
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  
      
      - 其中有两种错误需要特殊处理：
      
      - ```json
          // 表示已有的knownRSS数据库中已经有相同rsslink的记录了
          {
              'state':'failed', "description": "first query existed with rsslink"
          }
          
          // 表示已有的knownRSS数据库中已经有相同的rsstitle的记录了
          {
              'state':'failed', "description": "first query existed with rsstitle"
          }
          ```




### /rssdb/removeKnownRSS

> 注意：该api用于debug！！！
>
> 管理员 直接删除一个已有的RSS

- 输入：

  ```json
  {
      'rssId':2 // rss标识符
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'description': 'success', 
          'state': 'success'
      }
      ```
      
  - 失败时：
  
      ```json
      {
          'state':'failed', // 失败状态
          "description": "second query failed with error: " // 失败描述
      }
      ```
  







