# 测试记录_by_zkc

> url : 'http://39.98.93.128:5001'



## 压力测试

### apach benchmark

> 选择了常用api进行测试



#### login

> 登录

- url : 'http://39.98.93.128:5001/rssdb/getAllRSS'
- `ab -v 500 -p post4login.txt -T application/x-www-form-urlencoded http://39.98.93.128:5001/user/login`，连接正常
  - ![image-20201213163400038](E:\大四上\软件工程\src\flask_server\压力测试_zkc.assets\image-20201213163400038.png)
- `ab -c 10 -n 10 -p post4login.txt -T application/x-www-form-urlencoded http://39.98.93.128:5001/user/login`
- ![image-20201213163316104](E:\大四上\软件工程\src\flask_server\压力测试_zkc.assets\image-20201213163316104.png)

#### getAllRSS

> 获取所有knownRSS数据

- url：'http://39.98.93.128:5001/rssdb/getAllRSS'
- `ab -c 100 -n 200 http://39.98.93.128:5001/rssdb/getAllRSS`

- ![image-20201213153430510](E:\大四上\软件工程\src\flask_server\压力测试_zkc.assets\image-20201213153430510.png)



#### userGetFavorRSS_links

> 获取某个用户的订阅RSS数据

- url : 'http://39.98.93.128:5001/userfavor/getFavorRSSlinks'
- `ab -v 500 -p post4userRSSlink.txt -T application/x-www-form-urlencoded http://39.98.93.128:5001/userfavor/getFavorRSSlinks`
- `ab -c 100 -n 500 -p post4userRSSlink.txt -T application/x-www-form-urlencoded http://39.98.93.128:5001/userfavor/getFavorRSSlinks`
- ![image-20201213163216286](E:\大四上\软件工程\src\flask_server\压力测试_zkc.assets\image-20201213163216286.png)