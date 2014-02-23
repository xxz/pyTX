# coding:utf-8
# file: TXCore for pyTX with Python
# written by xxz(xxz@live.cn) @2014.02.23 

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import time
import datetime
import platform
import os
import urllib2
from xml.dom import minidom
import smtplib
from email.mime.text import MIMEText

#sleep time
SLP_TIME = 300

#if field retry to get something
RETRY_NUM = 0
RETRY_TIMES = 3



class TXCore(object):
    def __init__(self):
        print('TXCore initialize...')
        self.logfile = 'TX'
        self.LOOKUPLINK='http://geoip.ubuntu.com/lookup'

    def show_Msg(self, msg):
        print '[%s] %s' % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), msg)

    def show_ErrMsg(self, msg):
        print '[%s] %s' % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), msg)

    def get_Time(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def get_IP(self):
        global RETRY_NUM
        global RETRY_TIMES


        try:
                self.show_Msg('try to get my ip')
                f = urllib2.urlopen(self.LOOKUPLINK)
        except:
                if RETRY_NUM >= RETRY_TIMES :
                    self.show_Msg('retry too many times, sleep %d second' % SLP_TIME)
                    time.sleep(SLP_TIME)
                    RETRY_NUM = 0
                else:
                    RETRY_NUM = RETRY_NUM + 1
                    return  self.get_IP()

        try:
                xmldoc = minidom.parse(f)
                node = xmldoc.childNodes[0]
                ipnode = node.childNodes[0]
        except:
                if RETRY_NUM >= RETRY_TIMES :
                    self.show_Msg('retry too many times, sleep %d second' % SLP_TIME)
                    time.sleep(SLP_TIME)
                    RETRY_NUM = 0
                else:
                    RETRY_NUM = RETRY_NUM + 1
                    return self.get_IP()


        return ipnode.firstChild.data


    def log_IP(self, IP):
        self.show_Msg('LogFile:'+self.logfile)
        try:
            self.show_Msg('Writing LogFile:'+self.logfile)
            logfile=open(self.logfile,'w')
        except IOError:
            self.show_ErrMsg('Error in open logfile')
            exit()

        logfile.write(IP)
        logfile.close()


    def set_LogFilePath(self, filename):
        if(platform.system() == 'Windows'):
            logfile_path=os.getenv('TEMP')+'\\'
        else:
            logfile_path='/tmp/'

        self.logfile=logfile_path+filename
