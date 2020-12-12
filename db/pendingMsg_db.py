# 调用自定义包: db, 具体路径在run.py同目录下的文件夹中, 操作数据库
# print(__main__)
# from sqlite3_db import DB
from db.sqlite3_db import DB

class pendingMsg(DB):
    def __init__(self, db_path = 'data/pendingMsg.sqlite'):
        self.db_path = db_path
        self.init_table_sql = '''
        CREATE TABLE IF NOT EXISTS "pendingMsg" ("_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE , "userID" VARCHAR, "rsslink" VARCHAR, "rsstitle" VARCHAR, "checkedByAdministrator" VARCHAR);
        '''
        super(pendingMsg, self).__init__(self.db_path, self.init_table_sql)
    
    def checkRSSlink(self,rsslink):
        self.cursor.execute("SELECT * FROM pendingMsg WHERE rsslink = '{}'".format(rsslink))
        outs = self.cursor.fetchall()
        if outs:
            return outs[0]
        else:
            return None
    
    def checkRSStitle(self,rsstitle):
        self.cursor.execute("SELECT * FROM pendingMsg WHERE rsstitle = '{}'".format(rsstitle))
        outs = self.cursor.fetchall()
        if outs:
            return outs[0]
        else:
            return None

    def addMsg(self, userID, rsslink, rsstitle):
        checklink_rst = self.checkRSSlink(rsslink)
        if checklink_rst == None:
            return {'state':'failed','msg':'existing rsslink'}
        
        checktitle_rst = self.checkRSStitle(rsstitle)
        if checktitle_rst == None:
            return {'state':'failed','msg':'existing rsstitle'}

        self.execute("INSERT INTO pendingMsg (userID,rsslink,rsstitle,checkedByAdministrator) VALUES (?,?,?,?)",(userID, rsslink, rsstitle, "None"))
        return {'state':'success','msg':'with return code: ' + str(self.cursor.lastrowid)}

    def receivedByAdministrator(self, administrator_id):
        self.cursor.execute("SELECT * FROM pendingMsg WHERE checkedByAdministrator = '{}'".format('None'))
        outs = self.cursor.fetchall()
        return outs

    def checkedByAdministrator(self, administrator_id, _id):
        self.cursor.execute("UPDATE pendingMsg set checkedByAdministrator = " + str(administrator_id) + " WHERE _id = {}".format(_id))
        return {'state':"success"}
        


    def selectAll(self):
        self.cursor.execute("SELECT * FROM pendingMsg")
        return self.cursor.fetchall()

if __name__ == "__main__":
    pendingMsg = pendingMsg()
    print("first print...")
    print(pendingMsg.selectAll())
    print(pendingMsg.oneUserAddArticle("admin","www.baidu.com","baidu"))
    print("second print...")
    print(pendingMsg.selectAll())
    print("third print...")
    print(pendingMsg.checkUserArticle("admin",'www.baidu.com',"baidu"))
    print("4th print...")
    print(pendingMsg.checkUserArticle("admin",'www.360.com',"baidu"))
    print(pendingMsg.selectOneUser("admin"))
    
    