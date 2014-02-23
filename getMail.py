import poplib
import email
import string

#class TSE_getMail(self):
#    """getting mail from dblogs"""
    


m = poplib.POP3('pop.163.com')
m.user('dblogs')
m.pass_('wearelove')
numMessage,size = m.stat()
hdr,message,octet=m.retr(numMessage)
#for j in m.retr(numMessage)[1]:
#    print j

mail=email.message_from_string(string.join(message,'\n')) 

content = mail.get_payload()
print content.split("\n",1)[-1]

m.quit()
