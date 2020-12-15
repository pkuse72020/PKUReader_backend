# UserManagement 模块说明

### 概述

本模块用于管理用户的注册、登录行为。在服务器端使用MD5加密存储用户密码。

### 用户注册
传入username、password，返回用户序列号userid。userid作为用户的唯一标识，在后续登录时使用。

失败返回值格式为{"state":"failed","description":...}
成功返回值格式为{"state":"success","userid":...}

### 用户登录
传入userid，username，password。首先查找是否存在此用户,存在则在服务器数据库中查找此id对应的用户数据条目。如果找到多条则表明服务器数据库出错。如果只找到一条，则检查用户传入的username时候和数据库的username一致，不一致也报错。最后检查密码是否正确，正确则予以登录，否则报错。

失败返回值格式为{"state":"failed","description":...}
成功返回值格式为{"state":"success"}