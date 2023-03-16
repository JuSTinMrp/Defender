def block_msg(msg_id):

        mail.create('Blocked')
        mail.copy(msg_id, 'Blocked')
        mail.store(msg_id, '+FLAGS', '\\Deleted')
        mail.expunge()          #permanently deleting the mail from the mail box(OPTIONAL)
        print()
        print("Blocking a mail....!")
        print(f"The email(s) with Message-ID {0} have been blocked.".format(msg_id))
        print()

def spam_msg(msg_id):

        mail.copy(msg_id,'Spam')
        mail.store(msg_id, '+FLAGS', '\\Deleted')  #flag marked as deleted 
        mail.expunge()
        print()
        print("Deleting a mail....!")
        print(f"The email(s) with Message-ID {0} have been deleted.".format(msg_id))
        print()


import imaplib
import email
from email.header import decode_header
import datetime as dt
import time

def banner():
    print()
    print('''                       dBBBBb  dBBBP  dBBBBP dBBBP  dBBBBb  dBBBBb  dBBBP dBBBBBb
                          dB'                          dBP     dB'            dBP
                     dBP dB' dBBP   dBBBP  dBBP   dBP dBP dBP dB' dBBP    dBBBBK'
                    dBP dB' dBP    dBP    dBP    dBP dBP dBP dB' dBP     dBP  BB 
                   dBBBBB' dBBBBP dBP    dBBBBP dBP dBP dBBBBB' dBBBBP  dBP  dB' 
                                                                                 ''')
    print()
banner()
acc = "testingguys619@gmail.com"
passwd = "jrkyjxtcjwxewtvq"

imap = imaplib.IMAP4_SSL("imap.gmail.com",993)      #imap4 cls with ssl

imap.login(acc, passwd)
print()
print(" [*] Connecting to GmailBox via IMAP...... : {0}".format(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
print()

#print(imap.list())
imap.select("INBOX")    #[Gmail]/All Mail  --> to see all mails in mailbox

status, messages = imap.search(None, 'UNSEEN')      #ALL/UNSEEN
messages = messages[0].split(b' ')   #list of email ids
print(messages,"\n")



num_msgs = len(messages[0].split())
print("Total number of unread mails in mailbox: ",num_msgs)


for msg_id in messages[0].split():
        status, message_data = imap.fetch(msg_id, "(BODY.PEEK[HEADER])")   #BODY[HEADER] -> mail status to seen
                                                                     #BODY.PEEK[HEADER]) -> fetch out the mail details and return status as unseen
        
        header = message_data[0][1].decode('utf-8')           #both produces same data
        msg = email.message_from_bytes(message_data[0][1])

        #print(header)
        print("+"*40,"\n")
        print(msg)
        


        From, encoding = decode_header(msg["From"])[0]
        if isinstance(From, bytes):         # if it's a bytes type, decode to str
            From = From.decode(encoding)
        To=msg["To"]
        Subject=msg["Subject"]
        Date=msg["Date"]

        print("Mailbox: INBOX")
        print("From:", From)
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("Date:", msg["Date"])
        print("="*50)
        print()



        #time.sleep(10)


    
imap.close()
imap.logout()

