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

acc = "testingguys619@gmail.com"
passwd = "jrkyjxtcjwxewtvq"

imap = imaplib.IMAP4_SSL("imap.gmail.com",993)      #imap4 cls with ssl

imap.login(acc, passwd)
print()
print(" [*] Connecting to GmailBox via IMAP...... : {0}".format(dt.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
print()

#print(imap.list())
imap.select("INBOX")

status, messages = imap.search(None, 'UNSEEN')      #ALL/UNSEEN

num_msgs = len(messages[0].split())
print("Total number of unread mails in mailbox: ",num_msgs)


for msg_id in messages[0].split():
        status, header = imap.fetch(msg_id, "(BODY.PEEK[HEADER])")
        
        msg = email.message_from_bytes(header[0][1])
        
        print("Mailbox: INBOX")
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("Date:", msg["Date"])
        print("="*50)
        print()


###################################################################################
while True:
    status, messages = imap.search(None, 'UNSEEN')
    messages = messages[0].split(b' ')   #list of email ids

    for mail in messages:
        res, msg = imap.fetch(mail, "(RFC822)")

        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])

                # decode the email subject
                subject = decode_header(msg["Subject"])[0][0]
                if isinstance(subject, bytes):
                    # if it's a bytes type, decode to str
                    subject = subject.decode()

                # decode email sender
                From, encoding = decode_header(msg["From"])[0]
                if isinstance(From, bytes):
                    # if it's a bytes type, decode to str
                    From = From.decode(encoding)

                print("Subject:", subject)
                print("From:", From)
                print("-"*10)
    
    time.sleep(10)
##################################################################################

    
imap.close()
imap.logout()

