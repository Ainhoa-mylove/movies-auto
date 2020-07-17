import pymysql
import hashlib
import time


class Database:
    def __init__(self,host='localhost',port=3306,
                 user='root',passwd='123456',
                 database='moviesky',charset='utf8'):
        self.host=host
        self.port=port
        self.user=user
        self.passwd=passwd
        self.database=database
        self.charset=charset
        self.connect_db()

    def connect_db(self):
        self.db=pymysql.connect(host=self.host,
                                port=self.port,
                                user=self.user,
                                passwd=self.passwd,
                                database=self.database,
                                charset=self.charset)

    def do_register(self,name,passwd):
        sql="select * from user where name='%s'"%name
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return False
        hash=hashlib.md5((name+'AKB48').encode())
        hash.update(passwd.encode())
        sql="insert into user (name,passwd) values (%s,%s)"
        try:
            self.cur.execute(sql,[name,hash.hexdigest()])
            self.db.commit()
            return True
        except Exception:
            return False

    def do_login(self,name,passwd):
        sql="select * from user where name='%s' and passwd='%s'"
        hash=hashlib.md5((name+'AKB48').encode())
        hash.update(passwd.encode())
        sql=sql%(name,hash.hexdigest())
        self.cur.execute(sql)
        r=self.cur.fetchone()
        if r:
            return True
        else:
            return False


    def create_cur(self):
        self.cur=self.db.cursor()

    def close(self):
        self.db.close()
