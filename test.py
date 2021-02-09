# from datetime import datetime
# now = datetime.now()

# a = str(now.date())
# y = str(now.year)
# m = str(now.month)

# if int(m) < 10:
#     m = '0'+m

# print('>>',y+m)
##################################################################################################

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group.member']
# SCOPES = ['https://www.googleapis.com/auth/admin.directory.group']

def members_groups(GROUP):
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
    print('Getting the names of members of a groups')
    results = service.members().list(maxResults=50, groupKey = GROUP).execute()
    members = results.get('members', [])
    #El primer miembro es la cabeza del diccionario por lo que no se tiene en cuenta
    #members = members[1:]
    list_id_members = []
    if not members:
        print('No members in the domain.')
    else:
        #print('Groups:')
        for member in members:
            if member['type'] == 'CUSTOMER':
                continue
            else:
                #print(u'{0}, {1}'.format(member['email'], member['id']))
                list_id_members.append(member['email'])
        return list_id_members

# Función para crear permisos a carpetas
def create_permissions(EMAIL_ADDRESS, ID_DRIVE):
    """
    EMAIL_ADRESS: Permisos que otorgora 
                (normalmente es un usuario por medio de un email 
                o un grupo de usuarios)
    ID_DRIVE: ID del Drieve que se asignan los permisos
    """
    try:
        permission = {'role': 'writer', 
                      'type' : 'group', 
                      'emailAddress': EMAIL_ADDRESS}
        drive.permissions().create(fileId=ID_DRIVE, body=permission).execute()
        return print('Permission Assigned!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Asignar acceso de todos los usuarios a un Proyecto (folder)
def assign_permissions_folder(LIST_PERMISSIONS, ID_FOLDER):
    for j in LIST_PERMISSIONS:
        create_permissions(EMAIL_ADDRESS=j, ID_DRIVE=ID_FOLDER)

def manage_permissions():
    if 


if __name__ == '__main__':
    # GROUP: Grupo de cual queremos obtener la lista de miembros
    # 03cqmetx3x4zz9p >> Grupos TI, deberia ser Grupo; empleados@quantil.com.co, 03cqmetx3x4zz9p
    mg = members_groups(GROUP='03cqmetx3x4zz9p')
    # 1_vDU2bCsYd7SRYVEbXjpl8fbvC7H5Db1 >> folder Pruebas TIC, deberia ser el folder del proyecto que se acaba de crear
    assign_permissions_folder(LIST_PERMISSIONS=mg, ID_FOLDER='1_vDU2bCsYd7SRYVEbXjpl8fbvC7H5Db1')
    print(mg)