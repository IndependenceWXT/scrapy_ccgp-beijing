# -*- coding: utf-8 -*-
import mysql.connector
from .settings import host,port,name,user,password,tablename
class CcgpBeijingPipeline:
    # 连接数据库
    def __init__(self):
        self.conn = mysql.connector.connect(host=host, port=port, database=name, user=user, password=password, charset='utf8')
        self.cs=self.conn.cursor()

    # 数据表是否存在
    def tableExists(self):
        stmt = 'SHOW TABLES LIKE "{}"'.format(tablename)
        print(stmt)
        self.cs.execute(stmt)
        return self.cs.fetchone()
    # 数据库操作
    def process_item(self, item, spider):
        if self.tableExists():
            print("不建数据表")
        else:
            print("创建数据表")
            creat_sql="CREATE TABLE {} (url VARCHAR(100),title VARCHAR(250),ctime datetime,gtime datetime,content text)".format(tablename)
            self.cs.execute(creat_sql)
            print("创建成功")
        # 插入数据
        sql="insert into news(url,title,ctime,gtime,content) values (%s,%s,%s,%s,%s)"
        # 提交sql语句
        self.cs.execute(sql,(item['url'],item['title'],item['ctime'],item['gtime'],item['content']))
        self.conn.commit()
        return item







