#!/usr/bin/env python

import smtplib
import commands,time
from email.mime.text import MIMEText
import time,datetime
import urllib,urllib2
import cookielib
from xml.dom import minidom 
import smtplib
from email.mime.text import MIMEText
import platform
import os


mailto_list=["dblogs@163.com"]

mail_host="smtp.163.com"
mail_user="dblogs"
mail_pass="wearelove"
mail_postfix="163.com"


#sleep time
SLP_TIME = 300

#if field retry to get something 
RETRY_NUM = 0
RETRY_TIMES = 3


LOOKUPLINK='http://geoip.ubuntu.com/lookup'

global IPINFO
global LOG_FILEPATH
global LOG_FILENAME
LOG_FILENAME='pyTX'




def showMsg(msg):
    print '[%s] %s' % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), msg)


def showErrMsg(msg):
    print '[%s] %s' % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), msg)


def getTime():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 


#delivery time
DELIVERY_TIME = getTime()

def get_IP(url):
    global RETRY_NUM
    global RETRY_TIMES

    try:
            showMsg('Running get_IP()')
            f = urllib2.urlopen(url)
    except:
            if RETRY_NUM >= RETRY_TIMES :
                showErrMsg('retry too many times, sleep %d second' % SLP_TIME)
                time.sleep(SLP_TIME)
                RETRY_NUM = 0
            else:
                RETRY_NUM = RETRY_NUM + 1
                return get_IP(url)
        
    try:            
            xmldoc = minidom.parse(f)
            node = xmldoc.childNodes[0]
            ipnode = node.childNodes[0]
    except:
            if RETRY_NUM >= RETRY_TIMES :
                showErrMsg('retry too many times, sleep %d second' % SLP_TIME)
                time.sleep(SLP_TIME)
                RETRY_NUM = 0
            else:
                RETRY_NUM = RETRY_NUM + 1
                return get_IP(url)
        
        
    return ipnode.firstChild.data



def send_mail(to_list, sub, content):
    '''
    to_list: send to somebody
    sub: subject
    content: content
    send_mail ("dblogs", "sub", "content")
    '''
    try:
        #content = content+commands.getoutput("ifconfig tun0 | grep inet | awk '{print $2}'")
        content = IPINFO
    except:
        print showErrMsg('There is a probleam at get ip info')


    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg=MIMEText(content)
    msg['Subject'] = DELIVERY_TIME
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

def log_ip(logfile_path):
    showMsg('LogFile:'+logfile_path)
    try:
        showMsg('Writing LogFile:'+logfile_path)
        logfile=open(logfile_path,'w')
    except IOError:
        showErrMsg('Error in open logfile')
        exit()

    logfile.write(IPINFO)
    logfile.close()

def set_IPinfo():
    showMsg('Running set_IPinfo()')
    global IPINFO
    IPINFO=get_IP(LOOKUPLINK)
    return True

def set_LogFilePath():
    if(platform.system() == 'Windows'):
        logfile_path=os.getenv('TEMP')+'\\'
    else:
        logfile_path='/tmp/'

    global LOG_FILEPATH
    LOG_FILEPATH=logfile_path+LOG_FILENAME
    return True

###True: IP must log to mail
###False: Has no changed 
def check_IPStatic():
    if os.path.isfile(LOG_FILEPATH):  
        showMsg('Running check_IPStatic()')
        try:
            logfile=open(LOG_FILEPATH,'r')
        except IOError:
            showErrMsg('Error in open logfile')
            check_IPStatic()

        ip=logfile.readline()
        if ip==IPINFO:          
            return False
        else:
            return True
    else:
        showMsg('Frist running checker\n\t\t\tRunning check_IPStatic()')
        log_ip(LOG_FILEPATH)
        if send_mail(mailto_list,"subject",""): 
            showMsg('Deliver mail sucess!')
            exit()
        else:
            showMsg('Delivery mail failure!')
 
if __name__ == '__main__':
    set_IPinfo()
    set_LogFilePath()
    if(check_IPStatic()):
        if send_mail(mailto_list,"subject",""): 
            showMsg('Deliver mail sucess!')
            exit()
        else:
            showMsg('Delivery mail failure!')
    else:
        showMsg('IP has no changed')
