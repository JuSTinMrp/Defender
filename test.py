import imaplib
import email
from email.header import decode_header
import datetime as dt
import time

acc = "testingguys619@gmail.com"
passwd = "jrkyjxtcjwxewtvq"

imap = imaplib.IMAP4_SSL("imap.gmail.com",993)      #imap4 cls with ssl

imap.login(acc, passwd)
print()
print(" [*] Connecting to GmailBox via IMAP...... : {0}".format(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
print()

#print(imap.list())
imap.select("INBOX")





tmp, messages = imap.search(None, 'ALL')
for num in messages[0].split():
	tmp, data = imap.fetch(num, '(RFC822)')


while(True):

    status, messages = imap.search(None, 'UNSEEN')  #ALL/UNSEEN
    #messages = messages[0].split(b' ')
    print(messages)
    print()
    print("Status: ",status)
    print()

    i=0
    for num in messages[0].split():
        status, data = imap.fetch(num, '(RFC822)')      #defines an electronic message format consisting of header fields and an optional message body.
        #print('Message: {0}\n'.format(data[0][1]))
	       
        print(status)
        print("Header of %d Unseen Mail" %i)
        i+=1
        print(data)
        print()
        print()
        break

    print("Status after 20 seconds...")
    time.sleep(20)
    print()

            
imap.close()
imap.logout()

