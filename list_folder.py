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

page_token = None
flag_while = True
flag_for = False
id_project = None
while flag_while:
    response = drive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                          spaces='drive',
                                          fields='nextPageToken, files(id, name)',
                                          pageToken=page_token).execute()
    for file in response.get('files', []):
        # Process change
        if file.get('name') == 'Proyectos y Trabajos':
            print('Encontrado')
            print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
            id_project = file.get('id')

            flag_while = False
            flag_for = True
    page_token = response.get('nextPageToken', None)
    if page_token is None:
       break

if flag_for == False:
    print('No se encontro Carpeta con ese nombre')
print('ID de la carpeta: ',id_project)