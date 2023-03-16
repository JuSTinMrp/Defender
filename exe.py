import imaplib
import email
from email.header import decode_header
import re
import itertools

# User credentials
username = "testingguys619@gmail.com"
password = "jrkyjxtcjwxewtvq"

# IMAP settings
imap_server = "imap.gmail.com"
imap_port = 993

# Connect to the IMAP server
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)
mail.select("inbox")

# Search for emails
typ, data = mail.search(None, "UNSEEN")
i = len(data[0].split())

for num,x in zip(data[0].split(),range(i)):
    # Fetch email header
    typ, header = mail.fetch(num, "(BODY.PEEK[HEADER])")

    # Parse email header
    msg = email.message_from_bytes(header[0][1])
    message_id = msg["Message-ID"]
    sender_name, encoding = decode_header(msg["From"])[0]
    if encoding:
        sender_name = sender_name.decode(encoding)
    try:
        sender_email = re.search(r"<(.+?)>", msg["From"]) #.group(1)
    except:
        sender_email = re.search(r"<(.+?)>", msg["From"]) #.group(1)


    receiver_email = re.search(r"<(.+?)>", msg["To"]) #.group(1)
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


    file_name = "email_" + str(x) + ".txt"
    output_file = open(file_name, 'w')
    output_file.write("Message ID: %s\n\nSender Name: %s\n\nSender Email: %s\n\nReceiver Email: %s\n\nDate and Time: %s\n\nSubject: %s\n\nBody Content: \n\n%sHTML Content: \n\n%sSPF Information: \n\n%sAuthentication Results: %s\n\nDKIM Signature: %s\n\nX-Google-DKIM: %s\n\nMessage State: %s\n\nARC-Authentication-Results: %s\n\nARC-Message-Signature: %s\n\n" %(message_id,sender_name,sender_email,receiver_email,date_time,subject,body_content,html_content,spf,auth_results, dkim_signature,xgoogle_dkim, message_state, arc_auth_results, arc_message_signature))
    output_file.close()
