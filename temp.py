# Get the header of the first unread email
status, message_data = mail.fetch(message_numbers[0], '(BODY[HEADER])')

# Extract the header from the message data
header = message_data[0][1].decode('utf-8')



import imaplib
import email

# account credentials
username = "your_email@gmail.com"
password = "your_password"

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL("imap.gmail.com")

# authenticate
imap.login(username, password)

# get list of mailbox folders
status, mailbox_list = imap.list()

# iterate over mailbox folders
for mailbox in mailbox_list:
    # select the mailbox folder
    mailbox_name = mailbox.decode().split()[-1]
    imap.select(mailbox_name)
    
    # search for unseen messages
    status, messages = imap.search(None, "UNSEEN")
    
    # iterate over unseen messages
    for msg_id in messages[0].split():
        # fetch the header of the message
        status, header = imap.fetch(msg_id, "(BODY.PEEK[HEADER])")
        
        # convert header bytes to message object
        msg = email.message_from_bytes(header[0][1])
        
        # print message headers
        print(f"Mailbox: {mailbox_name}")
        print("From:", msg["From"])
        print("To:", msg["To"])
        print("Subject:", msg["Subject"])
        print("Date:", msg["Date"])
        print("="*40)
        
# close the mailbox and logout
imap.close()
imap.logout()


##########################################################################################

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




######################################################################################33


import imaplib
import email
import re

# Connect to the IMAP server
imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
username = 'your_email_address'
password = 'your_email_password'
imap_server.login(username, password)

# Select the mailbox you want to fetch headers from
mailbox = 'INBOX'
imap_server.select(mailbox)

# Define the search criteria to fetch headers
search_criteria = '(UNSEEN)'
result, data = imap_server.search(None, search_criteria)

# Loop through the emails and fetch headers
for num in data[0].split():
    result, data = imap_server.fetch(num, '(BODY[HEADER])')
    email_message = email.message_from_bytes(data[0][1])
    
    # Extract the required fields from the email header
    message_id = email_message['Message-ID']
    name = email_message['From'].split('<')[0].strip('"').strip()
    sender_mail = email.utils.parseaddr(email_message['From'])[1]
    receiver_mail = email.utils.parseaddr(email_message['To'])[1]
    date = email.utils.parsedate_to_datetime(email_message['Date'])
    time = date.strftime("%H:%M:%S")
    subject = email_message['Subject']
    body_content = ""
    html_content = ""
    sender_ip_address = ""
    receiver_id_address = ""
    spf_information = ""
    dkim_information = ""
    dmarc_information = ""
    x_received = ""
    arc_seal = ""
    arc_message = ""
    signature = ""
    arc_authentication = ""
    results = ""
    received_spe = ""
    authentication_results = ""
    dkim_signature = ""
    xgoogle_dkim = ""
    x_gm = ""
    message_state = ""
    x_google_smtp_source = ""
    mime_version = ""
    content_type = ""
    
    # Extract the required fields from the email body
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body_content = part.get_payload(decode=True).decode('utf-8')
            elif part.get_content_type() == 'text/html':
                html_content = part.get_payload(decode=True).decode('utf-8')
    else:
        body_content = email_message.get_payload(decode=True).decode('utf-8')
        
    # Extract the required fields from the email header and body using regex
    pattern = re.compile(r'(Sender IP:)(.*)')
    match = re.search(pattern, body_content)
    if match:
        sender_ip_address = match.group(2).strip()
        
    pattern = re.compile(r'(Receiver ID:)(.*)')
    match = re.search(pattern, body_content)
    if match:
        receiver_id_address = match.group(2).strip()
        
    pattern = re.compile(r'(SPF:)(.*)')
    match = re.search(pattern, body_content)
    if match:
        spf_information = match.group(2).strip()
        
    pattern = re.compile(r'(DKIM-Signature:)(.*)')
    match = re.search(pattern, body_content)
    if match:
        dkim_information = match.group(2).strip()
        
    pattern = re.compile(r'(DMARC:)(.*)')
    match = re.search(pattern, body_content)
    if match:
        dmarc_information = match.group(2).strip()
        
    pattern = re.compile(r'(X-Received:)(.*)')
    match = re.search(pattern, str(email_message))
    if





########################################################################################33


import imaplib
import email
import re

# Set up the connection to the IMAP server
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your_email_address', 'your_password')
mail.select('inbox')

# Search for all email messages in the inbox
typ, data = mail.search(None, 'ALL')
msg_ids = data[0].split()

# Iterate over each email message and fetch its header
for msg_id in msg_ids:
    typ, data = mail.fetch(msg_id, '(BODY[HEADER])')
    raw_header = data[0][1].decode('utf-8')
    header = email.message_from_string(raw_header)

    # Extract various information from the header
    message_id = header['Message-ID']
    name = header['From'].split('<')[0].strip()
    sender_mail = re.search(r'<(.+)>', header['From']).group(1)
    receiver_mail = header['To']
    date = header['Date']
    time = re.search(r'\d{2}:\d{2}:\d{2}', date).group(0)
    subject = header['Subject']

    # Extract information related to SPF, DKIM, DMARC, and their signatures
    spf_info = header.get('Received-SPF')
    dkim_info = header.get('DKIM-Signature')
    dmarc_info = header.get('Authentication-Results')
    signatures = {
        'ARC-Seal': header.get('ARC-Seal'),
        'ARC-Message-Signature': header.get('ARC-Message-Signature'),
        'ARC-Authentication-Results': header.get('ARC-Authentication-Results'),
        'DKIM-Signature': header.get('DKIM-Signature'),
        'X-Google-DKIM-Signature': header.get('X-Google-DKIM-Signature'),
        'ARC-Authentication-Results': header.get('ARC-Authentication-Results'),
        'ARC-Message-Signature': header.get('ARC-Message-Signature')
    }

    # Extract information related to X-Received, Results, and Authentication-Results
    x_received = header.get('X-Received')
    results = header.get('Results')
    auth_results = header.get('Authentication-Results')

    # Extract information related to the message body
    typ, data = mail.fetch(msg_id, '(BODY[TEXT])')
    body_content = data[0][1].decode('utf-8')
    html_code = None
    if header.get_content_type() == 'multipart/alternative':
        for part in header.get_payload():
            if part.get_content_type() == 'text/html':
                html_code = part.get_payload(decode=True).decode('utf-8')
    elif header.get_content_type() == 'text/html':
        html_code = header.get_payload(decode=True).decode('utf-8')

    # Extract information related to MIME-Version and Content-Type
    mime_version = header.get('MIME-Version')
    content_type = header.get('Content-Type')

    # Print all the extracted information
    print('Message ID:', message_id)
    print('Name:', name)
    print('Sender Email:', sender_mail)
    print('Receiver Email:', receiver_mail)
    print('Date:', date)
    print('Time:', time)
    print('Subject:', subject)
    print('SPF Information:', spf_info)
    print('DKIM Information:', dkim_info)
    print('DMARC Information:', dmarc_info)
    print('Sign






######################################################################################

import imaplib
import email
from email.header import decode_header
import re

# User credentials
username = "your_email_address"
password = "your_email_password"

# IMAP settings
imap_server = "imap.gmail.com"
imap_port = 993

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)
mail.select("inbox")

# Search for emails
typ, data = mail.search(None, "ALL")
for num in data[0].split():
    # Fetch email header
    typ, header = mail.fetch(num, "(BODY[HEADER])")

    # Parse email header
    msg = email.message_from_bytes(header[0][1])
    message_id = msg["Message-ID"]
    sender_name, encoding = decode_header(msg["From"])[0]
    if encoding:
        sender_name = sender_name.decode(encoding)
    sender_email = re.search(r'<(.+?)>', msg["From"]).group(1)
    receiver_email = re.search(r'<(.+?)>', msg["To"]).group(1)
    date_time = msg["Date"]
    subject, encoding = decode_header(msg["Subject"])[0]
    if encoding:
        subject = subject.decode(encoding)

    # Fetch email body
    typ, body = mail.fetch(num, "(BODY[TEXT])")

    # Parse email body
    body_content = body[0][1].decode("utf-8")
    html_content = re.search(r'Content-Type: text/html;\s*charset="UTF-8"\s*(.*?)\s*--', body_content, re.DOTALL)
    if html_content:
        html_content = html_content.group(1).strip()

    # Fetch email authentication headers
    typ, auth_header = mail.fetch(num, "(BODY[HEADER.FIELDS (Received-Spf Authentication-Results Dkim-Signature X-Google-Dkim X-Gm-Message-State Arc-Authentication-Results Arc-Message-Signature Arc-Authenticity-Results Arc-Seal)])")
    auth_header = email.message_from_bytes(auth_header[0][1])

    # Parse email authentication headers
    spf = auth_header.get("Received-Spf")
    auth_results = auth_header.get("Authentication-Results")
    dkim_signature = auth_header.get("Dkim-Signature")
    xgoogle_dkim = auth_header.get("X-Google-Dkim")
    message_state = auth_header.get("X-Gm-Message-State")
    arc_auth_results = auth_header.get("Arc-Authentication-Results")
    arc_message_signature = auth_header.get("Arc-Message-Signature")
    arc_authenticity_results = auth_header.get("Arc-Authenticity-Results")
    arc_seal = auth_header.get("Arc-Seal")

    # Print email information
    print("Message ID:", message_id)
    print("Sender Name:", sender_name)
    print("Sender Email:", sender_email)
    print("Receiver Email:", receiver_email)
    print("Date and Time:", date_time)
    print("Subject:", subject)
    print("Body Content:", body_content)
    print("HTML Content:", html_content)
    print("SPF Information:", spf)
    print("Authentication Results:", auth_results)
    print("DKIM Signature:", dkim_signature)
    print("X-Google-DKIM:", xgoogle_dkim)
    print("Message State:", message_state)
    print("ARC-Authentication-Results:", arc_auth_results)
    print("ARC-Message-Signature:", arc_message_signature)
