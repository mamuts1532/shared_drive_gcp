import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors

def main():    
    #Credenciales y parametros para autenticación con API DRIVE 
    # Lo cambie de ruta, no se ha provado
    CLIENT_SECRET_FILE = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
    SCOPES=["https://www.googleapis.com/auth/drive"]

    flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials=flow.run_console()
    drive=build("drive", "v3", credentials=credentials)

    print('Autenticado valida con Api Drive V3')


    # Encontrar carpeta pde proyectos
    def search_folder():

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

                        flag_while = False
                        flag_for = True
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            if flag_for == False:
                print('No se encontro Carpeta con ese nombre')
            print('ID de la carpeta: ',id_project)
            return id_project
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None

    #Lista de carpetas que se crearan
    list_folder = ['Directores y Administrativos','Directores y Dirección Administrativa','Directores Generales y Administrativos', 'Administrativos', 'Todo Quantil']
    #Lista de metadatos de cada carpeta creada
    list_metadata = []
    searchfolder = search_folder()
    print('=>>',type(searchfolder))
  

    # Función para crear carpetas
    def create_folder(ID_PARENTS):
        print('>>',ID_PARENTS)
        try: 
            for lf in list_folder:
                file_name = {
                    'name': lf,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents':[ID_PARENTS], # Esta sera la carpeta padre, si se comenta se crearan las carpetas en la unidad principal

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

    if searchfolder != None:
        create_folder(ID_PARENTS = searchfolder)
    else:
        ('No hay carpeta con el nombre: Proyectos y Trabajos')

if __name__=='__main__':
    main()