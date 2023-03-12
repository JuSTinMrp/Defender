import requests
import json
import re
import email
import imaplib
from bs4 import BeautifulSoup

# Define the malicious email criteria
malicious_criteria = {
    "ip_addresses": ["127.0.0.1", "192.168.1.1"],
    "domains": ["example.com", "malicious.com"],
    "virustotal_score": 5,
    "url_analysis": {
        "waybackurls": ["malware.com"],
        "getallurls": ["phishing.com"]
    },
    "content_pattern": "banking information",
    "content_pattern_ignore_case": True
}

# Connect to the mailbox
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('your-email@gmail.com', 'your-password')
mail.select('inbox')

# Search for all emails in the mailbox
status, data = mail.search(None, 'ALL')

# Loop through all emails in the mailbox
for email_id in data[0].split():
    # Fetch the email content
    status, data = mail.fetch(email_id, '(RFC822)')
    email_content = data[0][1]

    # Parse the email content using the email module
    msg = email.message_from_bytes(email_content)

    # Get the email headers
    headers = dict(msg.items())

    # Check if the email is malicious based on the defined criteria
    is_malicious = False
    if "Received" in headers:
        received_header = headers["Received"]
        ip_addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', received_header)
        for ip_address in ip_addresses:
            if ip_address in malicious_criteria["ip_addresses"]:
                is_malicious = True
                break
    if "From" in headers:
        from_header = headers["From"]
        domains = re.findall(r'@[\w\.]+', from_header)
        for domain in domains:
            domain = domain[1:]
            if domain in malicious_criteria["domains"]:
                is_malicious = True
                break
    if "X-VirusTotal" in headers:
        virus_total_header = headers["X-VirusTotal"]
        virus_total_score = int(virus_total_header.split("/")[0])
        if virus_total_score >= malicious_criteria["virustotal_score"]:
            is_malicious = True
    for url in malicious_criteria["url_analysis"]["waybackurls"]:
        if url in email_content:
            is_malicious = True
            break
    for url in malicious_criteria["url_analysis"]["getallurls"]:
        if url in email_content:
            is_malicious = True
            break
    if malicious_criteria["content_pattern_ignore_case"]:
        content_pattern = re.compile(malicious_criteria["content_pattern"], re.IGNORECASE)
    else:
        content_pattern = re.compile(malicious_criteria["content_pattern"])
    if content_pattern.search(email_content):
        is_malicious = True

    # Block the email if it is malicious
    if is_malicious:
        mail.store(email_id, '+FLAGS', '\\Deleted')

# Close the mailbox connection
mail.expunge()
mail.close()
mail.logout()
