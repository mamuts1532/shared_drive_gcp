import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from uuid import uuid4

#Credenciales y parametros para autenticación con API DRIVE 
# Lo cambie de ruta, no se ha provado
CLIENT_SECRET_FILE = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticado valida con Api Drive V3')




# Función para crear Unidades Compartidas
def create_drive(name_drive):
    try: 
        
        request_id = str(uuid4())
        file_name = {
            "kind": "drive#drive",
            'name': name_drive,
            'mimeType': 'application/vnd.google-apps.folder',
            #'parents':['1_vDU2bCsYd7SRYVEbXjpl8fbvC7H5Db1'], # Esta sera la carpeta padre, si se comenta se crearan las carpetas en la unidad principal

        }
        obj = drive.drives().create(body=file_name, requestId = request_id).execute()

        print('Folders Created!!!')
        return obj['id']
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para dar permisos de administrador a unidades compartidas
def permissions_admin(ID,USER_ADMIN):
    try:        
        permission = {'kind':'"drive#permission"',
                        'role': 'organizer', 
                        'type' : 'user', 
                        'emailAddress': USER_ADMIN
                        }
        drive.permissions().create(fileId=ID,body=permission,  supportsAllDrives = True).execute()
        return print('Admin Permission Assigned!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para dar permisos de administrador de contenido a unidades compartidas
def permissions_admin_content(ID,USER_ADMIN_CONTENT):
    try:        
        permission = {'kind':'"drive#permission"',
                        'role': 'fileOrganizer', 
                        'type' : 'user', 
                        'emailAddress': USER_ADMIN_CONTENT
                        }
        drive.permissions().create(fileId=ID,body=permission,  supportsAllDrives = True).execute()
        return print('Admin Content Permission Assigned!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

if __name__=='__main__':
    print('Creating Folders...')
    #print('******************')
    a = create_drive(name_drive='AAAA')
    print('ID: ', a)
    #print('Assigning Permissions...')
    #print('******************')
    permissions_admin(ID=a,USER_ADMIN='jorge841124@gmail.com')
    permissions_admin_content(ID=a,USER_ADMIN_CONTENT='jorge.guevara@quantil.com.co')

# Para ser Admin en una unidas: 'role': 'organizer'
# Para ser Admin de contenido: 'role': 'fileOrganizer'


# https://developers.google.com/drive/api/v3/manage-shareddrives
# https://developers.google.com/drive/api/v3/about-shareddrives
# https://developers.google.com/drive/api/v3/manage-sharing
# https://developers.google.com/drive/api/v3/manage-shareddrives
# https://developers.google.com/drive/api/v3/reference/permissions
