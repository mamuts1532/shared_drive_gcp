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
list_folder = ['folderA','folderB','folderC']
#Lista de metadatos de cada carpeta creada
list_metadata = []

list_members_permissions = ['christian.urcuqui@quantil.com.co', 'cristian.sanchez@quantil.com.co', 'jorge.guevara@quantil.com.co', 'julian.nino@quantil.com.co']
folders = ['1NBj8x5uyBxF3qHtSbEK7I9_AOnYwMJ-a', '10HFXx1Q67JO-T6vaHZDnJD_lT4UZdeoE', '1B-mZh12qXbGwYoQdSnK-0_9ignRyPyzs']

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
            
        return list_metadata
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None


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

# Función para obtener permisos de carpetas
def get_permissions(ID_DRIVE, ID_PERMISSIONS):
    """
    ID_PERMISSIONS: Permisos que se consultara 
                (normalmente es un usuario por medio de un email 
                o un grupo de usuarios)
    ID_DRIVE: ID del Drieve que se consultara
    """
    try:
        gt = drive.permissions().get(fileId=ID_DRIVE, permissionId=ID_PERMISSIONS, fields='emailAddress, role').execute()
        #print(gt)
        return gt
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para eliminar permisos de carpetas
def delete_permissions(ID_PERMISSIONS, ID_DRIVE):
    """
    ID_PERMISSIONS: Permiso que se eliminara 
                (normalmente es un usuario por medio de un email 
                o un grupo de usuarios)
    ID_DRIVE: ID del Drieve al que se elimina algun permsiso
    """
    try:
        drive.permissions().delete(fileId=ID_DRIVE, permissionId=ID_PERMISSIONS).execute()
        return print('Permission Delete!!!')
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Función para listar permisos de carpetas
def list_permissions(ID_DRIVE):
    """
    ID_DRIVE: ID del Drieve que se consultara
    """
    try:
        listper = drive.permissions().list(fileId=ID_DRIVE).execute()
        return listper.get('permissions',[])
    except errors.HttpError as error:
        print('An error occurred:', error)
        return None

# Asignar acceso de todos los usuarios a un Proyecto (folder)
def assign_permissions_folder(LIST_PERMISSIONS, ID_FOLDER):
    for j in LIST_PERMISSIONS:
        create_permissions(EMAIL_ADDRESS=j, ID_DRIVE=ID_FOLDER)

def assign_permissions_excluding(LIST_PERMISSIONS, LIST_FOLDERS):
    for i in LIST_FOLDERS:
        for j in LIST_PERMISSIONS:
            create_permissions(EMAIL_ADDRESS=j, ID_DRIVE=i)






if __name__=='__main__':
    #assign_permissions_folder(LIST_PERMISSIONS=list_members_permissions,ID_FOLDER='1_vDU2bCsYd7SRYVEbXjpl8fbvC7H5Db1')    
    # lp = list_permissions(ID_DRIVE='1N-pCKaDlWc9oZOhWFa9Nt_6yqMqhvsWj')    
    # for i in lp:
    #     gp = get_permissions(ID_DRIVE='1N-pCKaDlWc9oZOhWFa9Nt_6yqMqhvsWj', ID_PERMISSIONS=i['id'])
    #     print('>>',gp['emailAddress'], gp['role'])

    print(list_permissions(ID_DRIVE='1YLF3sI5ClkFlWuqEI1eWWKweIl8qOfbQ'))
    








# https://developers.google.com/drive/api/v3/reference/files
# https://stackoverflow.com/questions/54162891/google-drive-api-v3-change-file-permissions-and-get-publicly-shareable-link-pyt
# https://developers.google.com/drive/api/v3/reference/permissions/create
# https://stackoverflow.com/questions/13244750/httperror-httperror-400-when-requesting-https-www-googleapis-com-bigquery-v2