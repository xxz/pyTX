# coding:utf-8
# file: TXData for pyTX with Python
# written by xxz(xxz@live.cn) @2014.02.23 

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


import sqlite3

class TXData(object):

    def __init__(self, DBname):
        print('TXData initialize...')
        self.DBname = DBname
        self.conn = sqlite3.connect(DBname+'.sqlite3')
        self.conn.text_factory = lambda x: unicode(x, utf-8, replace)
        self.curs = self.conn.cursor()

    def create_tbl(self,tbl_name, tbl_col):
        createsql = 'CREATE TABLE if not exists %s ( %s );' % (tbl_name, tbl_col)
        print(createsql)
        self.curs.execute(createsql)
        self.conn.commit()



isinstancename='test'

test = TXData( isinstancename )
test.create_tbl( isinstancename, 'username VARCHAR(20) UNIQUE,password VARCHAR(32),groupno INTEGER' )