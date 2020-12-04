import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from datetime import datetime



def main():    
    #Credenciales y parametros para autenticación con API DRIVE 
    # Lo cambie de ruta, no se ha provado
    CLIENT_SECRET_FILE = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
    SCOPES=["https://www.googleapis.com/auth/drive"]

    flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    credentials=flow.run_console()
    drive=build("drive", "v3", credentials=credentials)

    print('Autenticación valida con Api Drive V3')

    def time_string():
        now = datetime.now()
        y = str(now.year)
        m = str(now.month)
        return str(y+m)


    # Encontrar carpeta pde proyectos
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

                        flag_while = False
                        flag_for = True
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break

            if flag_for == False:
                print('No se encontro Carpeta con ese nombre')
            #print('ID de la carpeta: ',id_project)
            return id_project
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None
  

    # Función para crear carpetas
    def create_folder(ID_PARENTS, LIST_FOLDER):
        try: 
            for lf in LIST_FOLDER:
                file_name = {
                    'name': lf,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents':[ID_PARENTS], # Esta sera la carpeta padre, si se comenta se crearan las carpetas en la unidad principal

                }
                obj = drive.files().create(body=file_name).execute()
                #print('ls: ', type(obj))
                list_metadata.append(obj)

            #print('Id FOlder1: ',l[0]['id'])
            #print('Folders Created!!!')
            return list_metadata
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None

    # Función para dar permisos a carpetas
    def permissions(EMAIL_ADDRESS, ID_DRIVE):
        try:
            permission = {'role': 'writer', 
                        'type' : 'group', 
                        'emailAddress': EMAIL_ADDRESS}
            drive.permissions().create(fileId=ID_DRIVE, body=permission).execute()
            return 
        except errors.HttpError as error:
            print('An error occurred:', error)
            return None

    def assign_permissions(LIST_METADATA):
        for l in LIST_METADATA:
            if l['name'] == 'Directores y Administrativos':
                EMAIL_ADDRESS1 = 'director.area@quantil.com.co'
                EMAIL_ADDRESS2 = 'administrativo@quantil.com.co'
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS1, ID_DRIVE=l['id'])
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS2, ID_DRIVE=l['id'])
                

            elif l['name'] == 'Directores y Dirección Administrativa':
                EMAIL_ADDRESS1 = 'director.area@quantil.com.co'
                EMAIL_ADDRESS2 = 'direccion.administrativa@quantil.com.co'
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS1, ID_DRIVE=l['id'])
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS2, ID_DRIVE=l['id'])

            if l['name'] == 'Directores Generales y Administrativos':
                EMAIL_ADDRESS1 = 'director.general@quantil.com.co'
                EMAIL_ADDRESS2 = 'administrativo@quantil.com.co'
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS1, ID_DRIVE=l['id'])
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS2, ID_DRIVE=l['id'])

            if l['name'] == 'Administrativos':
                EMAIL_ADDRESS = 'administrativo@quantil.com.co'
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS, ID_DRIVE=l['id'])

            if l['name'] == 'Todo Quantil':
                EMAIL_ADDRESS = 'empleados@quantil.com.co'
                permissions(EMAIL_ADDRESS=EMAIL_ADDRESS, ID_DRIVE=l['id'])
    
    def search_folder(Id_Customer):

        page_token = None
        # flag_while = True
        # flag_for = False
        # id_project = None

        try:
            while True:
                response = drive.files().list(q = "'" + Id_Customer + "' in parents and trashed = false and mimeType='application/vnd.google-apps.folder'", 
                                              pageToken=page_token, 
                                              fields="nextPageToken, files(id, name)").execute()
                #items = results.get('files', [])
                dict_folder = {}
                for file in response.get('files', []):
                    # print('Encontrado')
                    print ('Cliente encontrado: %s' % file.get('name'))
                    dict_folder[file.get('name')] = file.get('id') 
                Project_new = input("¿Para qué cliente quiere crear un nuevo proyecto?, escriba el nombre como aparece en la lista! \n")
                count = 0
                while count < 2:

                    if Project_new in dict_folder:
                        return dict_folder[Project_new]
                    else:
                        print ('No se encontro Cliente con ese nombre')
                        Project_new = input("Por favor escriba nuevamente el nombre como aparece en la lista! \n")
                        count += 1   
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
        except errors.HttpError as error:
            print('An error occurred:', error)
    
    #Lista de carpetas que se crearan
    list_folder = ['Directores y Administrativos',
                   'Directores y Dirección Administrativa',
                   'Directores Generales y Administrativos', 
                   'Administrativos',
                   'Todo Quantil']
    #Lista de metadatos de cada carpeta creada
    list_metadata = []
    searchfolder = search_drive()

    if searchfolder != None:
        var_search_folder = search_folder(Id_Customer=searchfolder)
        if var_search_folder != None:
            name_project = input("Escriba el nombre del proyecto! \n")
            time_string = time_string()
            name_project = time_string+'-'+name_project
            list_name_project = [str(name_project)]
            var_folder_project = create_folder(ID_PARENTS=var_search_folder, LIST_FOLDER = list_name_project)
            var_folder_project_permissions = create_folder(ID_PARENTS = var_folder_project[0]['id'], LIST_FOLDER=list_folder)
            #assign_permissions(LIST_METADATA=var_folder_project_permissions)
        else:
            print('No se encontro Cliente con este Nombre!')
            
    else:
        print('No hay carpeta con el nombre: Proyectos y Trabajos')



if __name__=='__main__':
    main()


# Referencias:

# https://datatofish.com/executable-pyinstaller/