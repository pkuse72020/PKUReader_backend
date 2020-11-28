# RSS_Reader 后端

## 实现功能

- [ ] RSSHUB本地化
  - [ ] 本地部署 （都要尝试，通过rsshub doc里的部署）
  - [ ] 自定义新RSS route （优先级低）
- [ ] RSS阅读相关，参考https://github.com/smoqadam/PyFladesk-rss-reader
  - [ ] 添加新RSS源 （sqlite3）（0）
  - [ ] 获取新内容 （feedparser，图片、表格的具体展示方式需要和前端对接）（3）
  - [ ] 内容检索 （数据库的操作，需要设计搜索）（2）
- [ ] 关键词查询相关
  - [ ] 中文wiki本地部署、wiki关键词查询（3）
  - [ ] 文章分词、关键词提取（2）
- [ ] 用户管理相关
  - [ ] 登陆注册（1）
  - [ ] 收藏文章内容、收藏RSS（建立两个很简单的表）（1）
  - [ ] 分享
  - [ ] 评论
- [ ] web页面设计
  - [ ] pyQt5或electron实现桌面端

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
