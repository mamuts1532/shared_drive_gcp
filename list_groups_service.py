from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

def groups(CUSTOMER, DOMAIN):
    """Shows basic usage of the Admin SDK Directory API.
    Prints the names of groups.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/jorgeda/Downloads/Quantil/private/Directory_API_Quantil.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('admin', 'directory_v1', credentials=creds)

    # Call the Admin SDK Directory API
    print('Getting the names of groups in the domain')
    results = service.groups().list(customer= CUSTOMER, maxResults=50, domain=DOMAIN,
                                orderBy='email').execute()
    groups = results.get('groups', [])

    if not groups:
        print('No groups in the domain.')
    else:
        print('Groups:')
        for group in groups:
            print(u'{0}, {1}'.format(group['email'], group['id']))


if __name__ == '__main__':
    groups(CUSTOMER='03u2psid',DOMAIN='quantil.com.co')


# Referencias 


# https://developers.google.com/admin-sdk/directory/v1/guides/authorizing
# https://developers.google.com/admin-sdk/directory/reference/rest/v1/groups/list
# https://developers.google.com/admin-sdk/directory/v1/guides/manage-groups