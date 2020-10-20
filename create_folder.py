import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors

#Credenciales y parametros para autenticación con API DRIVE 
# Lo cambie de ruta, no se ha provado
CLIENT_SECRET_FILE = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticado valida con Api Drive V3')

#Lista de carpetas que se crearan
list_folder = ['folder1','folder2','folder3']
#Lista de metadatos de cada carpeta creada
list_metadata = []

# Función para crear carpetas
def create_folder():
    try: 
        for lf in list_folder:
            file_name = {
                'name': lf,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents':['1_vDU2bCsYd7SRYVEbXjpl8fbvC7H5Db1'], # Esta sera la carpeta padre, si se comenta se crearan las carpetas en la unidad principal

            }
            obj = drive.files().create(body=file_name).execute()
            #print('ls: ', type(obj))
            list_metadata.append(obj)

        #print('Id FOlder1: ',l[0]['id'])
        return print('Folders Created!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para dar permisos a carpetas
def permissions():
    try:
        permission = {'role': 'writer', 'type' : 'user', 'emailAddress': 'jorge841124@gmail.com'}
        drive.permissions().create(fileId=list_metadata[0]['id'],body=permission).execute()
        return print('Permission Assigned!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

if __name__=='__main__':
    print('Creating Folders...')
    print('******************')
    create_folder()
    print('Assigning Permissions...')
    print('******************')
    permissions()


# https://developers.google.com/drive/api/v3/reference/files
# https://stackoverflow.com/questions/54162891/google-drive-api-v3-change-file-permissions-and-get-publicly-shareable-link-pyt
# https://developers.google.com/drive/api/v3/reference/permissions/create
# https://stackoverflow.com/questions/13244750/httperror-httperror-400-when-requesting-https-www-googleapis-com-bigquery-v2