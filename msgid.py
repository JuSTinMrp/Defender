import imaplib

# set up IMAP connection
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login('your_email@gmail.com', 'your_password')
imap_server.select('inbox')

# search for email by subject
subject = 'insert_email_subject_here'
typ, data = imap_server.search(None, 'SUBJECT', '"%s"' % subject)

# retrieve email message ID
if data[0]:
    email_id = data[0].split()[0]
    typ, data = imap_server.fetch(email_id, '(BODY[HEADER.FIELDS (MESSAGE-ID)])')
    message_id = data[0][1].decode().strip()
    print('Message ID:', message_id)

# close IMAP connection
imap_server.close()
imap_server.logout()
