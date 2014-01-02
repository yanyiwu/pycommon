# -*- coding: utf-8 -*-
import sys
import MySQLdb
import time
import logging


class MysqlClient:
    def __init__(self, host, user, passwd, db):
        self.mysql_ip = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.__SLEEP_TIME = 60

        self.__connect()
            
    def __connect(self):
        while True:
            try:
                self.conn = MySQLdb.connect(
                    host=self.mysql_ip, 
                    user=self.user, 
                    passwd= self.passwd,
                    db=self.db,
                    use_unicode=False,
                    charset='utf8')
                return
            except Exception,e:
                logging.critical('MySQLdb.Connection failed! error:[%s]' %e)
            time.sleep(self.__SLEEP_TIME)

    def insert_kvs(self, _table_name, _key_list, _value_list):
        keys_str = ','.join(map(lambda x : '`%s`' %x, _key_list))
        values_str = ','.join(map(lambda x : '"%s"' %x, _value_list))

        sql = 'insert into %s (%s) values (%s)' %(_table_name, keys_str, values_str)
        ret = self.execute_sql(sql)
        return ret

    def update_kvs(self, _table_name, _key_list, _value_list, _where_keys = [], _where_vals = []):
        set_sql = ', '.join(map(lambda x, y: "%s='%s'" %(x, y) if isinstance(y, str)else "%s=%s" %(x, y), _key_list, _value_list))
        sql = "update %s set %s" %(_table_name, set_sql)
        if _where_keys and _where_vals:
            sql += " where " + ' and '.join(map(lambda x, y: "%s='%s'" %(x, y) if isinstance(y, str) else "%s=%s" %(x, y), _where_keys, _where_vals))
        retn = self.execute_sql(sql)
        return retn

    def delete_kvs(self, _table_name, _where_keys , _where_vals ):
        sql = "delete from %s" %(_table_name)
        sql += " where " + ' and '.join(map(lambda x, y: "%s='%s'" %(x, y) if isinstance(y, str) else "%s=%s" %(x, y), _where_keys, _where_vals))
        ret = self.execute_sql(sql)
        return ret

    def execute_sql(self, sql):
        try:
            self.conn.ping()
        except Exception,e:
            logging.critical('conn.ping() failed! error:[%s]' %e)
            self.__connect()

        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            retn = cursor.rowcount
            cursor.close()
            self.conn.commit()
            return retn
        except Exception, e:
            self.conn.rollback() 
            logging.error("insert sql[%s] failed, error info[%s]" %(sql, e))
            return 0      

    def select_sql(self,sql):
        try:
            self.conn.ping()
        except Exception,e:
            logging.critical('conn.ping() failed! error:[%s]' %e)
            self.__connect()
        cursor = self.conn.cursor()
        try:
            ret = cursor.execute(sql)
            self.conn.commit()
            if not ret:
                logging.debug("sql[%s] return empty" %sql)
                cursor.close()
                return None
            res = cursor.fetchall()
            cursor.close()
            return res
        except Exception, e:
            self.conn.rollback() 
            logging.error("select sql[%s] failed, error info[%s]" %(sql, e))
            return False

    def close(self):
        self.conn.close()
if __name__ == '__main__':
    pass
