import os
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# set up API credentials
creds = Credentials.from_authorized_user_file(os.path.expanduser('path/to/credentials.json'), ['https://www.googleapis.com/auth/gmail.modify'])

# create Gmail API client
service = build('gmail', 'v1', credentials=creds)

# define message ID of email to mark as spam
message_id = 'insert_message_id_here'

# define request body to modify the message's labels
request_body = {
    'removeLabelIds': [],
    'addLabelIds': ['SPAM']
}

# modify message's labels
try:
    message = service.users().messages().modify(userId='me', id=message_id, body=request_body).execute()
    print('Message marked as spam: %s' % message['id'])
except HttpError as error:
    print('An error occurred: %s' % error)
