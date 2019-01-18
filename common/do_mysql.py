# -*- coding: utf-8 -*-
# @time     : 2019/1/11 0011 上午 11:48
# @Author   : yuxuan
# #file     : do_mysql.py

# 封装数据库操作类

import pymysql
from common.read_conf import ReadConfig
from common.basic_data import DoRegex, Context


class DoMysql:

    # 连接数据库常用第一步放初始化函数中
    def __init__(self):
        host = ReadConfig().get('mysql', 'host')
        port = ReadConfig().get_int('mysql', 'port')
        user = ReadConfig().get('mysql', 'user')
        pwd = ReadConfig().get('mysql', 'pwd')
        try:
            self.db = pymysql.connect(host=host, user=user, password=pwd, port=port, cursorclass=pymysql.cursors.DictCursor)    # cursorclass设置查询后返回字典格式
        except ConnectionError as e:
            raise e


    # 查询返回一条数据

    def fetch_one(self, sql):
        cursor = self.db.cursor()   # 建立游标
        cursor.execute(sql)         # 执行sql查询
        cursor.close()
        data = cursor.fetchone()   # 根据sql查询并返回一条数据
        return data


    def fetch_all(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        cursor.close()
        data = cursor.fetchall()
        return data


    def close(self):      # 关闭数据库连接
        self.db.close()



if __name__ == '__main__':
    sql = 'SELECT COUNT(*) FROM user_db.t_user_info;'
    result = DoMysql().fetch_one(sql)['COUNT(*)']
    print(type(result))








