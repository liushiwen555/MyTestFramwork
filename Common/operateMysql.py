# -*- coding: utf-8 -*-
# @Time     : 2020/11/29 3:06 下午
# @Author   : LiuShiWen

import traceback
import pymysql
from Common.getLog import logger
from Common.getConfig import Config


class MysqlObject(object):
    def __init__(self, host, user, password, dbname, port=3306):
        """
        :param host: 数据库所在服务器IP
        :param username: 数据库用户名
        :param passwd: 数据库密码
        :param dbname: 要使用的数据库名称
        :param port: 端口号
        """
        self.logger = logger("error")
        self._host = host
        self._user = user
        self._password = password
        self._dbname = dbname
        self._port = port
        try:
            self._conn = pymysql.connect(host=self._host, user=self._user, password=self._password,
                                   database=self._dbname, port=self._port, charset='utf8', autocommit=True)
        except:
            self.logger.error("请检查传入数据库参数是否正确")
            self.logger.error(traceback.format_exc())

    def __enter__(self):
        """调用with方法的入口"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """调用with方法结束时启动"""
        self._conn.close()

    def singleQuerySQL(self,sql,size=0):
        """
        查询数据（单条原生语句查询）
        :param sql: 传入查询的sql语句，type is string
        :param size: 返还结果的记录条数，不传时默认返还所有记录
        :return: self.count 返还查询记录总数据；self.result 返还查询记录结果
        """
        '''创建游标'''
        cur = self._conn.cursor(pymysql.cursors.DictCursor)
        try:
            if sql.startswith('select'):
                '''执行sql语句'''
                cur.execute(sql)
                '''统计查询结果的记录数'''
                self.count = cur.rowcount
                if size==0:
                    '''获取所有查询结果'''
                    self.result = cur.fetchall()
                elif size != 0:
                    self.result = cur.fetchall(size)
            return self.result
        except:
            self.logger.error("SQL错误，请检查SQL格式是否正确")
            self.logger.error(traceback.format_exc())
        finally:
            cur.close()

    def excuteSQL(self,sql):
        """
        执行增、删、改的sql语句
        :param sql:
        :return:
        """
        '''创建游标'''
        cur = self._conn.cursor()
        try:
            if sql.startswith('insert'):
                print('插入数据：{}'.format(sql))
                cur.execute(sql)
            elif sql.startswith('update'):
                print('更新数据：{}'.format(sql))
                cur.execute(sql)
            elif sql.startswith('delete'):
                print('删除数据：{}'.format(sql))
                cur.execute(sql)
        except:
            self.logger.error("SQL错误，请检查SQL格式是否正确")
            self.logger.error(traceback.format_exc())
        finally:
            cur.close()

    def excuteManySQL(self,sql,value_list):
        """
        执行多条DML语句
        :param sql: 增删改等SQL
        :param value_list: 参数值列表
        :return: rows 改动的记录条数
        """
        cur = self._conn.cursor()
        try:
            rows = cur.executemany(sql,value_list)
            return rows
        except:
            self.logger.error("SQL错误，请检查SQL格式是否正确")
            self.logger.error(traceback.format_exc())
        finally:
            cur.close()


if __name__ == '__main__':
    with MysqlObject(host='localhost',port=3306,user='root',password='liushiwen555',dbname='selenium_db') as mysql:
        sql = 'select * from user limit 2'
        res = mysql.singleQuerySQL(sql, 0)
        print(res)
        print(type(res))

    # xxxx自行替换成对应信息
    with MysqlObject(host="xxxx", user="xxxx", password="xxxx", dbname="xxxx") as session:
        sql_insert_many = 'insert into test.test (name) values (%s)'
        value_list = ["chen", "zc"]
        row = session.excuteManySQL(sql_insert_many, value_list)


