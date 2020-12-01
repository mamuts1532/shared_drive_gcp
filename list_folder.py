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

def search_folder(Id_Project):

    page_token = None
    # flag_while = True
    # flag_for = False
    # id_project = None

    try:
        while True:
            response = drive.files().list(q = "'" + Id_Project + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'", pageToken=page_token, fields="nextPageToken, files(id, name)").execute()
            #items = results.get('files', [])
            dict_folder = {}
            for file in response.get('files', []):
                # print('Encontrado')
                print ('Cliente encontrado: %s' % file.get('name'))
                dict_folder[file.get('name')] = file.get('id') 
            Project_new = input("¿Para qué cliente quiere crear un nuevo proyecto?, escriba el nombre como aparece en la lista! \n")
            if Project_new in dict_folder:
                return dict_folder[Project_new]
            else:
                print ('No se encontro Cliente con ese nombre')
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break
    except errors.HttpError as error:
        print('An error occurred:', error)

if __name__=='__main__':
    var = search_folder(Id_Project='1N-pCKaDlWc9oZOhWFa9Nt_6yqMqhvsWj')
    #print('ID de la carpeta: ', var)
