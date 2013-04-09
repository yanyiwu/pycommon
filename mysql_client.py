# -*- coding: utf-8 -*-
import sys
sys.path.insert(0,'/usr/ali/lib/python2.5/site-packages')
import MySQLdb
import global_define
from pylogger import logger
import time

class MysqlClient:
    def __init__(self):
        self.mysql_ip = global_define.MYSQL_IP
        self.user = global_define.MYSQL_USER
        self.passwd = global_define.MYSQL_PASSWD
        self.db = global_define.MYSQL_DB
        self.port = global_define.MYSQL_PORT
        self.wait_seconds = 60

        self.__connect()

        #self.conn = MySQLdb.Connection(
        #    host=self.mysql_ip, 
        #    # port=self.port,
        #    user=self.user, 
        #    passwd= self.passwd,
        #    db=self.db,
         #   use_unicode=False,
         #   charset='utf8')
            
    def __connect(self):
        while True:
            try:
                self.conn = MySQLdb.Connection(
                    host=self.mysql_ip, 
                    # port=self.port,
                    user=self.user, 
                    passwd= self.passwd,
                    db=self.db,
                    use_unicode=False,
                    charset='utf8')
                return
            except Exception,e:
                logger.critical('MySQLdb.Connection failed! error:[%s]' %e)
            time.sleep(self.wait_seconds)

    def insert(self, sql):
        try:
            self.conn.ping()
        except Exception,e:
            logger.critical('conn.ping() failed! error:[%s]' %e)
            self.__connect()

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            cursor.close()
            self.conn.commit()
            return True
        except Exception, e:
            self.conn.rollback() 
            logger.error("insert sql[%s] failed, error info[%s]" %(sql, e))
            return False      

    def select(self,sql):
        try:
            self.conn.ping()
        except Exception,e:
            logger.critical('conn.ping() failed! error:[%s]' %e)
            self.__connect()
        cursor = self.conn.cursor()
        try:
            ret=cursor.execute(sql)
            if ret:
                return cursor.fetchall()
            else:
                logger.error("%s:fetchall return 0 " %sql)
        except Exception, e:
            self.conn.rollback() 
            logger.error("select sql[%s] failed, error info[%s]" %(sql, e))
            return False

    def select_dict(self,sql):
        try:
            self.conn.ping()
        except Exception,e:
            logger.critical('conn.ping() failed! error:[%s]' %e)
            self.__connect()
        cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
        try:
            ret=cursor.execute(sql)
            if ret:
                return cursor.fetchall()
            else:
                logger.error("%s:fetchall return 0 " %sql)
        except Exception, e:
            self.conn.rollback() 
            logger.error("select sql[%s] failed, error info[%s]" %(sql, e))
            return False
        
           
    def close(self):
        self.conn.close()
if __name__ == '__main__':
    pass
