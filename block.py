import imaplib

# authenticate
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login('your_email@gmail.com', 'your_password')

# search for email
imap_server.select('inbox')
typ, data = imap_server.search(None, 'FROM', 'spam_sender@example.com')

# block email
for num in data[0].split():
    imap_server.store(num, '+FLAGS', '\\Deleted')

# expunge deleted emails
imap_server.expunge()

# close connection
imap_server.close()
imap_server.logout()
