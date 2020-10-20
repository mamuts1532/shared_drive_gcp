import pandas as pd
import numpy as np
import math

df = pd.read_excel('/home/jorgeda/Downloads/Gestion Drive MATFIN.xlsx')
df2 = df[['Nombre Drive','Admin','Acceso 1','Acceso 2','Acceso 3','Acceso 4','Acceso 5','Acceso 6','Acceso 7','Acceso 8']]

df3 = df2.head(2)

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
        elif j == 'Admin':
            if df3[j][i] == '' or pd.isnull(df3[j][i]):
                print('No hay usuario para asignar como admin general')
                
            else:
                nombre_usuario_admin = df3[j][i]
                print('Se llama la funcion para asignar el Admin General para la columna',j, 'y el usuario sera: ',nombre_usuario_admin)
        else:
            if df3[j][i] == '' or pd.isnull(df3[j][i]):
            #if not df3[j][i]:
                print('No hay usuario para asignar como admin de contenido')
                
            else:
                nombre_usuario_admin_content = df3[j][i]
                print('Se llama la funcion para asignar Admin de contenido',j, 'y el usuario sera: ',nombre_usuario_admin_content)

