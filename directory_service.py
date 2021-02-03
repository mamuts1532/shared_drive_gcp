from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def main():
    """Shows basic usage of the Admin SDK Directory API.
    Prints the emails and names of the first 10 users in the domain.
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
    print('Getting the first 10 users in the domain')
    results = service.users().list(customer='03u2psid', maxResults=50,
                                orderBy='email').execute()
    users = results.get('users', [])

    if not users:
        print('No users in the domain.')
    else:
        print('Users:')
        for user in users:
            print(u'{0} ({1})'.format(user['primaryEmail'],
                user['name']['fullName']))


if __name__ == '__main__':
    main()

















# Referencias 

# https://developers.google.com/apps-script/advanced/admin-sdk-directory
# https://www.youtube.com/watch?v=j2ha_o3q4Ik
# https://www.youtube.com/watch?v=twCrEHXdC4Q&t=182s
# https://developers.google.com/admin-sdk/directory/v1/guides/prerequisites?hl=es
# # https://developers.google.com/admin-sdk/directory/v1/get-start/getting-started?hl=es
# https://developers.google.com/admin-sdk/directory/v1/guides/manage-users?hl=es
# https://developers.google.com/admin-sdk/directory/reference/rest/v1/users/list?hl=es
