# 调用自定义包: db, 具体路径在run.py同目录下的文件夹中, 操作数据库
# print(__main__)
from sqlite3_db import DB
# from db.sqlite3_db import DB

class favorRSS_DB(DB):
    def __init__(self, db_path = 'data/favorRSS.sqlite'):
        self.db_path = db_path
        self.init_table_sql = '''
        CREATE TABLE IF NOT EXISTS "favorRSS" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "userID" VARCHAR, "RSS" VARCHAR, "RSS_name" VARCHAR);
        '''
        super(favorRSS_DB, self).__init__(self.db_path, self.init_table_sql)
    
    def selectOneUser(self, userID):
        self.cursor.execute("SELECT userID, RSS, RSS_name FROM favorRSS WHERE userID = '{}'".format(userID))
        outs = self.cursor.fetchall()
        return outs

    def checkUserRSS(self, userID, rss, rss_name):
        self.cursor.execute("SELECT * FROM favorRSS WHERE userID='{}' AND RSS='{}' AND RSS_name='{}'".format(userID,rss,rss_name))
        return self.cursor.fetchall()

    def oneUserRemoveRSS(self, userID, rss, rss_name):
        self.execute("DELETE FROM favorRSS WHERE userID='{}' AND RSS='{}' AND RSS_name='{}'".format(userID,rss,rss_name))

    def oneUserAddRSS(self, userID, rss, rss_name):
        check_rst = self.checkUserRSS(userID, rss, rss_name)
        # print("debug:>>>")
        # print(check_rst)
        # check_rst = []
        # print(not check_rst)
        if not check_rst:
            # print("debug")
            self.execute("INSERT INTO favorRSS (userID,RSS,RSS_name) VALUES (?,?,?)",(userID, rss, rss_name))
            return self.cursor.lastrowid
        else:
            return "existed"

    def selectAll(self):
        self.cursor.execute("SELECT * FROM favorRSS")
        return self.cursor.fetchall()

if __name__ == "__main__":
    favorRSS = favorRSS_DB()
    print("first print...")
    print(favorRSS.selectAll())
    print(favorRSS.oneUserAddRSS("admin","www.baidu.com","baidu"))
    print("second print...")
    print(favorRSS.selectAll())
    print("third print...")
    print(favorRSS.checkUserRSS("admin",'www.baidu.com',"baidu"))
    print("4th print...")
    print(favorRSS.checkUserRSS("admin",'www.360.com',"baidu"))
    print(favorRSS.selectOneUser("admin"))
    
    