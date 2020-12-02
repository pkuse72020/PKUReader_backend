# 调用自定义包: db, 具体路径在run.py同目录下的文件夹中, 操作数据库
# print(__main__)
# from sqlite3_db import DB
from db.sqlite3_db import DB

class favorArticle_DB(DB):
    def __init__(self, db_path = 'data/favorArticle.sqlite'):
        self.db_path = db_path
        self.init_table_sql = '''
        CREATE TABLE IF NOT EXISTS "favorArticle" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "userID" VARCHAR, "Article" VARCHAR, "Article_name" VARCHAR);
        '''
        super(favorArticle_DB, self).__init__(self.db_path, self.init_table_sql)
    
    def selectOneUser(self, userID):
        self.cursor.execute("SELECT userID, Article, Article_name FROM favorArticle WHERE userID = '{}'".format(userID))
        outs = self.cursor.fetchall()
        return outs

    def checkUserArticle(self, userID, Article, Article_name):
        self.cursor.execute("SELECT * FROM favorArticle WHERE userID='{}' AND Article='{}' AND Article_name='{}'".format(userID,Article,Article_name))
        return self.cursor.fetchall()

    def oneUserRemoveArticle(self, userID, Article, Article_name):
        self.execute("DELETE FROM favorArticle WHERE userID='{}' AND Article='{}' AND Article_name='{}'".format(userID,Article,Article_name))

    def oneUserAddArticle(self, userID, Article, Article_name):
        check_rst = self.checkUserArticle(userID, Article, Article_name)
        # print("debug:>>>")
        # print(check_rst)
        # check_rst = []
        # print(not check_rst)
        if not check_rst:
            # print("debug")
            self.execute("INSERT INTO favorArticle (userID,Article,Article_name) VALUES (?,?,?)",(userID, Article, Article_name))
            return self.cursor.lastrowid
        else:
            return "existed"

    def selectAll(self):
        self.cursor.execute("SELECT * FROM favorArticle")
        return self.cursor.fetchall()

if __name__ == "__main__":
    favorArticle = favorArticle_DB()
    print("first print...")
    print(favorArticle.selectAll())
    print(favorArticle.oneUserAddArticle("admin","www.baidu.com","baidu"))
    print("second print...")
    print(favorArticle.selectAll())
    print("third print...")
    print(favorArticle.checkUserArticle("admin",'www.baidu.com',"baidu"))
    print("4th print...")
    print(favorArticle.checkUserArticle("admin",'www.360.com',"baidu"))
    print(favorArticle.selectOneUser("admin"))
    
    