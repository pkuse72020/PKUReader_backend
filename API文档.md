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
      'articleId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e' // 文章id，用字符串表示数字，用于唯一确定文章，对应文章数据库中的id
  }
  ```

- 输出：

  - 成功时：

      ```json
      {
          'state': 'success', //成功状态
          'moreMsg': [{'_Id': 1, 'articleId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}], // 表示该添加内容在数据库中的项
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1, 
                   'articleId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', 
                   'userId': 'b7451baa-3eda-11eb-a877-00163e0f2f21',
                   'content': '  人民网北京12月15日电 （赵竹青）记者从国家航天局获悉，截至12月14日21时，“天问一号”探测器已在轨飞行144天，飞行里程约3.6亿公里，距离地球超过1亿公里，距离火星约1200万公里，飞行状态良好。   受天体运动规律影响，火星与地球距离在0.5亿公里至4亿多公里周期性发生变化。“天问一号”探测器到达火星附近时，距离地球约1.9亿公里。   “天问一号”自7月23日发射以来，已成功完成地月合照、探测器“自拍”、三次中途修正、一次深空机动、载荷自检等工作。后续，还将进行数次轨道修正，预计明年2月中旬接近火星后，实施“刹车”制动进入环火轨道，为火星着陆作准备。', 
                 'keywords': {'0': '火星', '1': '距离', '2': '探测器', '3': '地球', '4': '深空', '5': '机动', '6': '天问', '7': '附近', '8': '修正', '9': '环火', '10': '赵竹青', '11': '北京', '12': '记者', '13': '人民网', '14': '国家航天局', '15': '轨道', '16': '规律', '17': '载荷', '18': '天体', '19': '周期性'}, 
                 'title': '“天问一号”距地球超1亿公里 预计明年2月抵达火星'
                }], // 列表，每一项表示一条数据库记录
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // user标识符，用于唯一确定用户的字符串
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // user标识符，用于唯一确定用户的字符串
      'RSSId':'1' // RSSid，用字符串表示数字，用于唯一确定RSS，对应RSS数据库中的id
  }
  ```

- 输出：

  - 成功时：

      ```json
      {
          'state': 'success', //成功状态
          'moreMsg': [{'_Id': 9, 'rssId': 1, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}], // 表示该添加内容在数据库中的项
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1, 'rssId': 1, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                  {'_Id': 2, 'rssId': 2, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                  {'_Id': 3, 'rssId': 5, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                  {'_Id': 4, 'rssId': 6, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                {'_Id': 5, 'rssId': 7, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                {'_Id': 6, 'rssId': 10, 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}], // 数据库内容
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // user标识符，用于唯一确定用户的字符串
  }
  ```
  
- 输出：

  - 成功时：

      ```json
      {
          'rst': [{'_Id': 1, // 这个没用，或许可以用来排序
                   'rssId': 1, // 该rss的标识符
                   'rsslink': 'https://rss.injahow.cn/zhihu/people/activities/li-xi-mo-66',
                   'rsstitle': 'liximo66的知乎',
                   'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'},
                  {'_Id': 2,
                   'rsslink': 'https://rss.injahow.cn/zhihu/hotlist',
                   'rsstitle': '知乎热搜',
                 'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // 用户标识符
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
                   'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}
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
      'userId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // 用户标识符
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
                       'userId': 'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e'}], // 该申请在数据库中的项的具体信息
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
      'administratorId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // 管理员id
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
      'administratorId':'bd6f7f6d-0b56-4ed5-9501-b829d8e78d3e', // 管理员id
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
  

## content

> 用于显示文章列表或搜索文章

### /content/getArticles

> 给用户生成一个推荐文章列表；如果用户已有关注的源则从源获取新文章，否则获取一些默认文章

- 输入：

  ```json
  {
      'userid': 'be19d186-3e9f-11eb-a877-00163e0f2f21'  //登录时返回的用户id，格式类似示例
  }
  ```

- 输出：

  ```json
  {
      'state':'success',
      'article_list':{
          '0':{
              'title': '文章名',
              'article': '文章正文',
              'id': 'a7ae6a6b-c1d7-48b6-8914-6054dfd3ac3c', //文章id，格式类似示例
              'keyword_num':20,
              'keyword_list':{
                  '0': '关键词1',
                  '1': '关键词2',
                  //...中间略
               	'19': '关键词20'
              },
              'imgLinks':['https://cn.bing.com/th?id=OHR.IbonPlan_ZH-CN8564017247_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
      'https://cn.bing.com/th?id=OHR.BarnettsDemesne_ZH-CN8484261440_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp'] // 图片链接列表，包含所有图片，若新闻没有图片则返回默认图片
          },
          '1':{
              'title': '文章名2',
              'article': '文章正文2',
              'id': 'id2', 
              'keyword_num':20,
              'keyword_list':{
                  '0': '关键词a',
                  '1': '关键词b',
                  //...中间略
               	'19': '关键词t'
          },
              'imgLinks':['https://cn.bing.com/th?id=OHR.IbonPlan_ZH-CN8564017247_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp',
      'https://cn.bing.com/th?id=OHR.BarnettsDemesne_ZH-CN8484261440_1920x1080.jpg&amp;rf=LaDigue_1920x1080.jpg&amp;pid=hp'] // 图片链接列表，包含所有图片，若新闻没有图片则返回默认图片
      }
          //后略
  }
  ```



### /content/search

> 用于关键词搜索文章；支持多关键词用空格分隔。

- 输入：

  ```json
  {
      'searchword': '我 爱 软件' //准备搜索的关键词
  }
  ```

  

- 输出：

  ```json
  {
      'state': 'success',
    'result': {
          '0': {
              'article': '文章内容',
              'title': '文章标题',
              'id': '文章id',
              'keyword_num': 20,
              'keyword_list':{
                  '0': '关键词1',
                  '1': //...
                  //...
                  
              }
          },
          '1':{
              //...与上面格式相同
          },
          //...
      }
  }
      
  //失败时：
  {
      'state': 'failed',
      'description': '....'
  }
  ```
  
  

### /content/getArticleById

> 用于通过文章id获得单篇文章内容

- 输入

  ```json
  {
  	'articleid': '文章id'	
  }
  ```

  

- 输出

  ```json
  {
      'title': '文章标题',
      'content': '文章内容',
      'keywords':{
          '0': '关键词1',
          '1': '关键词2',
          //...
      }
  }
  ```

  