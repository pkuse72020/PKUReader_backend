# 调用自定义包: db, 具体路径在run.py同目录下的文件夹中, 操作数据库
# print(__main__)
from sqlite3_db import DB
# from db.sqlite3_db import DB

class knownRSS_DB(DB):
    def __init__(self, db_path = 'data/knownRSS.sqlite'):
        self.db_path = db_path
        self.init_table_sql = '''
        CREATE TABLE IF NOT EXISTS "knownRSS" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "RSS_name" VARCHAR, "RSS" VARCHAR);
        '''
        super(knownRSS_DB, self).__init__(self.db_path, self.init_table_sql)
    
    def checkName(self,rss_name):
        self.cursor.execute("SELECT * FROM knownRSS WHERE RSS_name = '{}'".format(rss_name))
        outs = self.cursor.fetchall()
        if len(outs) == 0:
            return {"state":False, "rst":None}
        else:
            return {"state":True, "rst":outs[0]}

    def checkLink(self,rss):
        self.cursor.execute("SELECT * FROM knownRSS WHERE RSS = '{}'".format(rss))
        outs = self.cursor.fetchall()
        if len(outs) == 0:
            return {"state":False, "rst":None}
        else:
            return {"state":True, "rst":outs[0]}

    def name2link(self, rss_name):
        self.cursor.execute("SELECT RSS FROM knownRSS WHERE RSS_name = '{}'".format(rss_name))
        outs = self.cursor.fetchall()
        if len(outs) == 0:
            return None
        else:
            return outs[0]

    def link2name(self, rss):
        self.cursor.execute("SELECT RSS FROM knownRSS WHERE RSS = '{}'".format(rss))
        outs = self.cursor.fetchall()
        if len(outs) == 0:
            return None
        else:
            return outs[0]

    def printJson(self):
        self.cursor.execute("SELECT RSS_name, RSS FROM knownRSS")
        outs = self.cursor.fetchall()
        return outs

    def addlink(self, rss, rss_name):
        checkName_rst = self.checkName(rss_name)
        checkLink_rst = self.checkLink(rss)

        if checkName_rst['state'] == False and checkLink_rst['state'] == False:
            # print("debug")
            self.execute("INSERT INTO knownRSS (RSS_name,RSS) VALUES (?,?)",(rss_name, rss))
            return {"state":self.cursor.lastrowid,"rst":None}
        elif checkName_rst['state'] == True:
            return {"state":"existed","rst":checkName_rst['rst']}
        else:
            return {"state":"existed","rst":checkLink_rst['rst']}

    def removeLink(self, rss, rss_name):
        self.execute("DELETE FROM knownRSS WHERE RSS_name='{}' and RSS = '{}'".format(rss_name, rss))
    
if __name__ == "__main__":
    
    # TODO:

    knownRSS = knownRSS_DB()
    print("first print...")
    print(knownRSS.printJson())
    print(knownRSS.oneUserAddRSS("admin","www.baidu.com","baidu"))
    print("second print...")
    print(knownRSS.selectAll())
    print("third print...")
    print(knownRSS.checkUserRSS("admin",'www.baidu.com',"baidu"))
    print("4th print...")
    print(knownRSS.checkUserRSS("admin",'www.360.com',"baidu"))
    print(knownRSS.selectOneUser("admin"))
    
    