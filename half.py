import requests
import re
import os
import subprocess

# Header Analysis
def header_analysis(email):
    ip = re.findall(r'Received: from\s+([^\s]+)\s+\(', email)
    domain = re.findall(r'Received: from\s+[^\s]+\s+\(.*?\[([^\]]+)\]', email)
    return ip[-1], domain[-1]

# Link Analysis
def link_analysis(url):
    response = requests.get(url)
    if response.status_code == 200:
        virustotal = 'https://www.virustotal.com/gui/url/' + response.text.split('"')[1].strip()
        waybackurls = subprocess.check_output(['waybackurls', url]).decode('utf-8').strip()
        gau = subprocess.check_output(['gau', url]).decode('utf-8').strip()
        return virustotal, waybackurls, gau

# Content Checking
def content_checking(email):
    return 'confirm your bank account' in email.lower() or 'you have won' in email.lower()

# Block Email
def block_email(email_id):
    os.system('sudo postsuper -d ' + email_id)

# Main Program
if __name__ == '__main__':
    email = '''Received: from example.com ([127.0.0.1])
    by localhost (example.com [127.0.0.1]) (amavisd-new, port 10024)
    with ESMTP id KvzThRtSd0Op for <user@example.com>;
    Sat,  6 Mar 2023 10:00:00 +0000 (UTC)
    (envelope-from <spammer@example.com>)
    Received: from mail.example.com (mail.example.com [192.168.1.1])
    by example.com (Postfix) with ESMTPS id 123456789
    for <user@example.com>; Sat,  6 Mar 2023 10:00:00 +0000 (UTC)
    (envelope-from <spammer@example.com>)
    Received: from mail.example.com (localhost.localdomain [127.0.0.1])
    by mail.example.com (Postfix) with ESMTP id 123456789
    for <user@example.com>; Sat,  6 Mar 2023 10:00:00 +0000 (UTC)
    (envelope-from <spammer@example.com>)
    Message-ID: <123456789>
    Date: Sat, 6 Mar 2023 10:00:00 +0000 (UTC)
    From: spammer@example.com
    To: user@example.com
    Subject: Important Message
    X-Spam-Status: No, score=0.0 required=5.0 tests=none
    X-Spam-Level:
    X-Spam-Checker-Version: SpamAssassin 3.4.0 (2014-02-07) on example.com
    X-Virus-Scanned: amavisd-new at example.com
    Return-Path: <spammer@example.com>
    '''
    ip, domain = header_analysis(email)
    virustotal, waybackurls, gau = link_analysis(domain)
    content = content_checking(email)
    if content or ('positives' in requests.get(virustotal).text):
        email_id = re.findall(r'^Message-ID:\s+<(.+)>', email, flags=re.MULTILINE)[-1]
        block_email(email_id)
        print
