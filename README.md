# RSS_Reader 后端

## 实现功能

- [x] RSSHUB本地化
  - [x] 本地部署 （都要尝试，通过rsshub doc里的部署）
  - [ ] 自定义新RSS route （优先级低）
- [x] RSS阅读相关，参考https://github.com/smoqadam/PyFladesk-rss-reader
  - [x] 添加新RSS源 （sqlite3）（0）
  - [x] 获取新内容 （feedparser，图片、表格的具体展示方式需要和前端对接）（3）
  - [x] 内容检索 （数据库的操作，需要设计搜索）（2）
- [x] 关键词查询相关
  - [x] 中文wiki本地部署、wiki关键词查询（3）
  - [x] 文章分词、关键词提取（2）
- [x] 用户管理相关
  - [x] 登陆注册（1）
  - [x] 收藏文章内容、收藏RSS（建立两个很简单的表）（1）
  - [ ] 分享（优先级低）
  - [ ] 评论（优先级低）
- [x] web页面设计
  - [ ] pyQt5或electron实现桌面端（优先级低）

## 部署方式
- 重建数据库`python run.py`，如遇权限问题可使用`sudo python run.py`，然后按`Ctrl+C`结束运行。数据库文件路径为`app/database.db`
- 启动gunicorn服务器`sh start_gunicorn.sh`，其参数在config.py中定义，其中在sh文件中需要写明gunicorn的路径
- 启动rsshub服务器需要在rsshub的代码路径下运行`sh start_rsshub.sh`，其中端口等信息定义在sh文件中
- `wiki.db`数据库文件过大，我们提供了小型的`data/wikidemo.db`作为样例，其中的表结构与实际使用的`wiki.db`相同，数据量上仅提供前1000行数据

## ElasticSearch安装与配置
- 从ElasticSearch官网下载安装ElasticSearch
- 安装ik分词器(https://github.com/medcl/elasticsearch-analysis-ik)
- 修改ElasticSearch的配置文件，允许外部访问
- 运行ElasticSearch

## Requirements

- nodejs for **RSSHUB**
- flask
- feedparser
- sqlite3
- ***[TO BE CONTINUED]***

## Reference
- 参考https://www.cnblogs.com/old-jipa-deng/p/12980427.html 中的优秀示例
  - https://www.cnblogs.com/SivilTaram/p/4900457.html
  - https://github.com/MinJieDev/Roadmap-Frontend
  - https://blog.csdn.net/waynelu92/article/details/73604172
- commit规范：https://github.com/youngjuning/conventional-commits-demo
