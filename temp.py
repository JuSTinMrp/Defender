import imaplib
import email
from email.header import decode_header
import time

# account credentials
username = "your_email@gmail.com"
password = "your_password"

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(username, password)

# select the mailbox you want to read
# if you want a specific mailbox use imap.select("Mailbox Name")
imap.select("inbox")

# continuously check for new emails
while True:
    # search for new email
    status, messages = imap.search(None, 'UNSEEN')

    # convert messages to a list of email IDs
    messages = messages[0].split(b' ')

    for mail in messages:
        # fetch the email message by ID
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

                # print the email headers
                print("Subject:", subject)
                print("From:", From)
                print("----")
    
    # wait for 10 seconds before checking for new emails again
    time.sleep(10)
    
# close the mailbox and logout
imap.close()
imap.logout()


##########################################################################################


import imaplib
import email
from email.header import decode_header

# account credentials
username = "testingguys619@gmail.com"
password = "-----------------"

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(username, password)

# select the mailbox you want to read
# if you want a specific mailbox use imap.select("Mailbox Name")
imap.select("inbox")

# search for specific email by subject
# result: list of email IDs
status, messages = imap.search(None, 'ALL')

# convert messages to a list of email IDs
messages = messages[0].split(b' ')

for mail in messages:
    # fetch the email message by ID
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

            # print the email headers
            print("Subject:", subject)
            print("From:", From)
            print("----")
            
# close the mailbox and logout
imap.close()
imap.logout()


#################################################################################33


import datetime
import email
import imaplib
import mailbox


EMAIL_ACCOUNT = "your@gmail.com"
PASSWORD = "your password"

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(EMAIL_ACCOUNT, PASSWORD)
mail.list()
mail.select('inbox')
result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
i = len(data[0].split())

for x in range(i):
    latest_email_uid = data[0].split()[x]
    result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    # result, email_data = conn.store(num,'-FLAGS','\\Seen') 
    # this might work to set flag to seen, if it doesn't already
    raw_email = email_data[0][1]
    raw_email_string = raw_email.decode('utf-8')
    email_message = email.message_from_string(raw_email_string)

    # Header Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
    email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
    subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))

    # Body details
    for part in email_message.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            file_name = "email_" + str(x) + ".txt"
            output_file = open(file_name, 'w')
            output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(email_from, email_to,local_message_date, subject, body.decode('utf-8')))
            output_file.close()
        else:
            continue
