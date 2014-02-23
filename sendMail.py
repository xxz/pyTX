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


def showMessage(msg):
    print '[%s] %s' % (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'), msg)


def getTime():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') 


#delivery time
DELIVERY_TIME = getTime()

def getIP(url):
    global RETRY_NUM
    global RETRY_TIMES
    
    try:
            showMessage('try to get my ip')
            f = urllib2.urlopen(url)
    except:
            if RETRY_NUM >= RETRY_TIMES :
                showMessage('retry too many times, sleep %d second' % SLP_TIME)
                time.sleep(SLP_TIME)
                RETRY_NUM = 0
            else:
                RETRY_NUM = RETRY_NUM + 1
                return getIP(url)
        
    try:            
            xmldoc = minidom.parse(f)
            node = xmldoc.childNodes[0]
            ipnode = node.childNodes[0]
    except:
            if RETRY_NUM >= RETRY_TIMES :
                showMessage('retry too many times, sleep %d second' % SLP_TIME)
                time.sleep(SLP_TIME)
                RETRY_NUM = 0
            else:
                RETRY_NUM = RETRY_NUM + 1
                return getIP(url)
        
        
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
        content = getIP(LOOKUPLINK)
    except:
        print showMessage('There is a probleam at get ip info')


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

if __name__ == '__main__':
    if send_mail(mailto_list,"subject",""): 
        showMessage('Deliver mail sucess!')
    else:
        showMessage('Delivery mail failure!')