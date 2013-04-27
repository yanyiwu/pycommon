# -*- coding: utf-8 -*-
import sys
import MySQLdb
from pylogger import logger
import time


class MysqlClient:
    def __init__(self, host, user, passwd, db):
        self.mysql_ip = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.wait_seconds = 60

        self.__connect()
            
    def __connect(self):
        while True:
            try:
                self.conn = MySQLdb.Connection(
                    host=self.mysql_ip, 
                    user=self.user, 
                    passwd= self.passwd,
                    db=self.db,
                    use_unicode=False,
                    charset='utf8')
                return
            except Exception,e:
                logger.critical('MySQLdb.Connection failed! error:[%s]' %e)
            time.sleep(self.wait_seconds)

    def insert_kvs(self, _table_name, _key_list, _value_list):
        keys_str = ','.join(map(lambda x : '`%s`' %x, _key_list))
        values_str = ','.join(map(lambda x : '"%s"' %x, _value_list))

        sql = 'insert into %s (%s) values (%s)' %(_table_name, keys_str, values_str)
        self.insert_sql(sql)
        logger.debug('insertdb sql[%s] finished.' %sql)

    def update_kvs(self, _table_name, _key_list, _value_list, _where_keys = [], _where_vals = []):
        #UPDATE persondata SET ageage=age*2, ageage=age+1; 
        set_sql = ', '.join(map(lambda x, y: "%s='%s'" %(x, y), _key_list, _value_list))
        sql = "update %s set %s" %(_table_name, set_sql)
        if _where_keys and _where_vals:
            sql += " where " + ', '.join(map(lambda x, y: "%s='%s'" %(x, y), _where_keys, _where_vals))
        self.insert_sql(sql)
        logger.debug('sql[%s] finished.' %sql)


    def insert_sql(self, sql):
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

    def select_sql(self,sql):
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

    def select_dict_sql(self,sql):
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
    client = MysqlClient("192.168.1.175", "wyy", "wyy123", "pingluntuan_log");
    #client.insert_sql("insert into req_analysis_test (day,req_sum) values ('2013-3-1',10)")
    client.update_kvs("req_analysis_test", ["req_sum"], ["22"], ["day"], ["20130301"])
    pass
