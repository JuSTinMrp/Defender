import imaplib
import email
from email.header import decode_header

# set up IMAP connection
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
imap_server.login('your_email@gmail.com', 'your_password')
imap_server.select('inbox')

# search for email by message ID
message_id = 'insert_message_id_here'
typ, data = imap_server.search(None, 'HEADER', 'Message-ID', '<%s>' % message_id)

# retrieve email message
if data[0]:
    email_id = data[0].split()[0]
    typ, data = imap_server.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]

    # parse email message
    email_message = email.message_from_bytes(raw_email)

    # print email header information
    for header_name in email_message.keys():
        header_value = email_message.get(header_name, '')
        header_decoded = decode_header(header_value)
        header_decoded_str = ''
        for value, encoding in header_decoded:
            if encoding:
                value = value.decode(encoding)
            else:
                value = value.decode()
            header_decoded_str += value
        print('%s: %s' % (header_name, header_decoded_str))

# close IMAP connection
imap_server.close()
imap_server.logout()
