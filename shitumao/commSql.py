#encoding:utf-8
import MySQLdb

class commSql:
    '''
                    有关于数据库操作的基础类，主要包含：
                        连接、关闭、读取、删除、增加数据
    '''
    def __init__(self,dbName,sql,dbIp,dbUserName,dbPwd):
        self.dbName = dbName
        self.sql = sql
        self.dbIp = dbIp
        self.dbUserName = dbUserName
        self.dbPwd = dbPwd
        
    def ConnectDB(self):
        '''连接时指定数据库名'''
        return MySQLdb.connect(dbIp,dbUserName,dbPwd,self.dbName,charset='utf8')
        
    def Common(self):
        '''添加数据、更新数据的基础方法'''
        cursor = db.cursor()
        try:
            cursor.execute(self.sql)
            db.commit()
        except:
            db.rollback()
            
    def Select(self):
        '''选取数据的基本方法,返回一个list，是一个对象'''
        cursor = db.cursor()
        try:
            cursor.execute(self.sql)
            results = cursor.fetchall()
            return results
        except:
            db.rollback()
            return 'false'
        
    def Close(self):
        '''关闭数据库连接'''
        db.close(self.dbName)
        