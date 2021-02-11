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

def search_drive():

    page_token = None
    flag_while = True
    flag_for = False
    id_project = None

    try:
        while flag_while:
            response = drive.files().list(q="mimeType='application/vnd.google-apps.folder'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                if file.get('name') == 'Proyectos y Trabajos':
                    # print('Encontrado')
                    # print ('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                    id_project = file.get('id')

                    #flag_while = False
                    #flag_for = True
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

        # if flag_for == False:
        #     print('No se encontro Carpeta con ese nombre')
        # print('ID de la carpeta: ',id_project)
        return id_project
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

if __name__=='__main__':
    var = search_drive()
    print('ID de la carpeta: ', var)


## Referencias 
# https://developers.google.com/drive/api/v2/reference/files/list
# https://developers.google.com/drive/api/v2/search-files
# https://stackoverflow.com/questions/56857760/list-of-files-in-a-google-drive-folder-with-python