import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import datetime
from apiclient import errors
from uuid import uuid4
import pandas as pd

#Credenciales y parametros para autenticación con API DRIVE 
# Lo cambie de ruta, no se ha provado
CLIENT_SECRET_FILE = "/home/jorgeda/Downloads/Quantil/private/drive_aut.json"
SCOPES=["https://www.googleapis.com/auth/drive"]

flow=InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials=flow.run_console()
drive=build("drive", "v3", credentials=credentials)

print('Autenticado valida con Api Drive V3')


# Función para crear Unidades Compartidas
def create_folder(name_drive):
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




df = pd.read_excel('/home/jorgeda/Downloads/Gestion Drive MATFIN.xlsx')
df3 = df[['Nombre Drive','Admin','Acceso 1','Acceso 2','Acceso 3','Acceso 4','Acceso 5','Acceso 6','Acceso 7','Acceso 8']]

#df3 = df2.head(2)

print('Longitud de DF',df3.shape)

for i in df3.index:

    
    columns = list(df3) 
  
    for j in columns:
        if j == 'Nombre Drive':
            if df3[j][i] == '' or pd.isnull(df3[j][i]):
                print('No hay nombre para asignar a la Unidad')
                
            else: 
                nombre_drive = df3[j][i]
                print('El nombre de la Unidad sera: ', nombre_drive)
                Id_drive = create_folder(name_drive=nombre_drive)
        elif j == 'Admin':
            if df3[j][i] == '' or pd.isnull(df3[j][i]):
                print('No hay usuario para asignar como admin general')
                
            else:
                nombre_usuario_admin = df3[j][i]
                print('Se llama la funcion para asignar el Admin General para la columna',j, 'y el usuario sera: ',nombre_usuario_admin)
                permissions_admin(ID=Id_drive,USER_ADMIN=nombre_usuario_admin)
        else:
            if df3[j][i] == '' or pd.isnull(df3[j][i]):
                print('No hay usuario para asignar como admin de contenido')
                
            else:
                nombre_usuario_admin_content = df3[j][i]
                print('Se llama la funcion para asignar Admin de contenido',j, 'y el usuario sera: ',nombre_usuario_admin_content)
                permissions_admin_content(ID=Id_drive,USER_ADMIN_CONTENT=nombre_usuario_admin_content)