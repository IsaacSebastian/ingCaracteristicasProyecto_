import os
import pandas as pd
import re
# Censos de Población y Vivienda

CENSOS_DE_POBLACION_Y_VIVIENDA_PATH="data/raw/DATOS EDUCACION/CENSOS DE POBLACION Y VIVIENDA"# Ruta en donde se encuentran los datos de Censos
work_directory=CENSOS_DE_POBLACION_Y_VIVIENDA_PATH

"""
Se extraen los datos a un dataframe por archivo, y se guardan en una lista.

"""
dataframes=[] # Lista de dataframes
diccionarios_de_datos=[]
for item in os.listdir(work_directory):
    if item==".DS_Store":
        continue
    item_path=f"{work_directory}/{item}"
    # En caso de tratarse de un archivo resultado de una extracción zip:
    if os.path.isdir(item_path):
        file_name=os.listdir(f"{item_path}/conjunto_de_datos")[0]
        file_path=f"{item_path}/conjunto_de_datos/{file_name}"
        df=pd.read_csv(file_path)
    # Se busca un archivo diccionario de datos y se guarda el dataframe de este en la lista de diccionarios
        pattern = r"^diccionario.*datos$"
        for subitem in os.listdir(item_path):
            match = re.search(pattern,subitem)
            if match:
                dictionary_name=match.group()
        dictionary= os.listdir(f'{item_path}/{dictionary_name}')[0]
        data_dictionary_path=f"{item_path}/{dictionary_name}/{dictionary}"
        dictionary_df=pd.read_csv(data_dictionary_path,encoding='ISO-8859-1')
        diccionarios_de_datos.append(dictionary_df)
    # En este caso particular, el resto de los archivos son de tipo excel
    else:
        file_path=item_path
        print(file_path)
        df=pd.read_excel(file_path,sheet_name=1,skiprows=4)
    
    dataframes.append(df)
    print(f"Datos del archivo {item} se cargaron a la lista 'dataframes' ")

#Ordenamos los dataframes en orden cronológico

dataframes_order_year=[]
for index in [3,5,6,1,7,8,9,0,4,2]:
    dataframes_order_year.append(dataframes[index])


def revision_nulos(df):
    """
    df:Dataframe que se quiere analizar

    Esta función recibe el dataframe que se quiere analizar para imprimir el porcentaje de registros nulos
    por cada columna del dataframe.
    """
    total_rows=len(df)
    for column in df.columns:
        nans=0
        nans=df[column].isna().sum()
        if nans!=0:
            print(f"{round(100*nans/total_rows,4)}% de los registros en {column} son nulos")


def formato_columnas(df,format_columns):
    """
    df:Dataframe que se quiere analizar
    format_columns: Diccionario en donde las llaves siguen la estructura '<tipo_dato>_columns' y los valores
    son listas de los nombres de las columnas que se quieren guardar bajo el tipo de dato de la llave.


    Esta función primero genera un diccionario donde las llaves son el nombre de la columna dentro
    del dataframe, y los valores son el tipo de dato en la que se quieren guardar. Luego, intenta 
    actualizar el tipo de dato que sigue cada columna. Si se encuentra con un error ValueError, 
    guarda la columna y el valor que causó el error en una lista llamada error_columns. Esta lista 
    es lo que entrega al final
    """
    formats={}
    for string_column in format_columns['string_columns']:
        formats[string_column]='str'

    for float_column in format_columns['float_columns']:
        formats[float_column]='float'

    for integer_column in format_columns['integer_columns']:
       formats[integer_column]='int'

    error_columns=[]
    for column,format_type in formats.items():
        try:
            df[column] = df[column].astype(format_type)
            #print(f"Columna {column} formateada a {format_type}")
        except ValueError as e:
            pattern = r"'(.*?)'"
            match = re.search( pattern, str(e) )
            error_value=match.group(1)
            error_columns.append([column,error_value]) 
    return error_columns

def filtro_columnas(df,dictionary_dataframe,columns):
    """
    df: Dataframe de los datos que se quieren utilizar
    diciontary_dataframe: Dataframe de diccionario de datos asociado con el dataframe en uso
    columns:Lista de columnas que se mantendran en el dataframe

    Esta función primero traduce los mnemónicos del dataframe en uso a sus nombres completos utilizando
    el dataframe del diccionario de datos. Luego, se filtran las clolumnas que se quieren usar en el d-
    ataframe original.

    """
    rename_dictionary={}
    for index,row in dictionary_dataframe.iterrows():
        old_column_name=row['mnemonico']
        new_column_name=row['indicador']
        rename_dictionary[old_column_name] = new_column_name

    df=df.rename(columns=rename_dictionary)
    df=df[columns]
    return df

processed_dataframes=[] # Aquí guardaremos los dataframes despues de procesar los datos

# Censo de 1950 : Población de 6 a 29 años que asisten a instituciones de enseñanza, por entidad federativa y sexo, según edad(1950)

df=dataframes_order_year[0]
unnamed_columns=df.columns.to_list()[3:10] # Columnas que no vienen nombradas correctamente por estructura en la que se guardo el excel.
rows_to_drop=[0,1,104,105] # Filas que no nos sirven, no contienen registro de alguna observación

# Renombramos las columnas que no tienen nombre, sus nombres se encuentran en la primera fila como resultado de la estructura en la que se guardo el archivo excel.
rename_dictionary={}
for column in unnamed_columns:
    rename_dictionary[column]=df[column][0] 

df=df.rename(columns=rename_dictionary)
df=df.drop(rows_to_drop)
 
# Guardamos las columnas al formato más consistente
format_columns=df.columns.to_list()[3:11]
for column in format_columns:
    df[column]=df[column].astype('int')

revision_nulos(df) # Si no imprime nada, significa que no se encontraron registros nulos

processed_dataframes.append(['1950',df])

# Censo 1960 : Población de 6 años y más, por entidad federativa, área urbana y rural, alfabetismo y sexo, según grupos de edad(1960)
df=dataframes_order_year[1]
# Renombrar columnas
unnamed_columns=df.columns.to_list()[6:18]
rename_dictionary={}
for column in unnamed_columns:
    rename_dictionary[column]=df[column][0]
df=df.rename(columns=rename_dictionary)

df=df.rename(columns={
    6.0:"6",
    7.0:"7",
    8.0:"8",
    9.0:"9",
})

extra_columns=df.columns.to_list()[6:18]
rename_dictionary={}
for column in extra_columns:
    rename_dictionary[column]=f"{column} años"
    df=df.rename(columns=rename_dictionary)

# Remover registros 
rows_to_drop=[0,1,893]
df=df.drop(rows_to_drop)


# Formatear columnas
format_columns=df.columns.to_list()[5:19]
for column in format_columns:
    df[column]=df[column].astype('int')

revision_nulos(df)

processed_dataframes.append(['1960',df])
df.info()

# Censo 1970 : Población de 6 años y más, por entidad federativa, tamaño de la localidad y grupos de edad, según condición de alfabetismo y sexo (1970)
df=dataframes_order_year[2]

# Renombrar columnas
unnamed_columns=df.columns.to_list()[4:]
rename_dictionary={}
for column in unnamed_columns[:2]:
    rename_dictionary[column]=f"Saben leer y escribir :{df[column][0]}"
for column in unnamed_columns[2:]:
    rename_dictionary[column]=f"No saben leer y escribir :{df[column][0]}"
    
df=df.rename(columns=rename_dictionary)


# Remover registros 
rows_to_drop=[0,1,1964]
df=df.drop(rows_to_drop)


# Formatear columnas
format_columns=df.columns.to_list()[4:]
for column in format_columns:
    df[column]=df[column].astype('int')

processed_dataframes.append(['1970',df])

# Censo 1980 : Población de 15 años y más, por entidad federativa, tamaño de localidad y grupos quinquenales de edad, según condición de alfabetismo y sexo (1980)
df=dataframes_order_year[3]

# Renombrar columnas
unnamed_columns=df.columns.to_list()[5:]
rename_dictionary={}
for column in unnamed_columns[:2]:
    rename_dictionary[column]=f"Alfabetas :{df[column][0]}"
for column in unnamed_columns[2:]:
    rename_dictionary[column]=f"Analfabetas :{df[column][0]}"
    
df=df.rename(columns=rename_dictionary)



# Remover registros 
rows_to_drop=[0,1,3181]
df=df.drop(rows_to_drop)


# Formatear columnas
format_columns=df.columns.to_list()[4:]
for column in format_columns:
    df[column]=df[column].astype('int')


processed_dataframes.append(['1980',df])


# Censo 1990 : Población de 6 a 14 años por entidad federativa y edad desplegada según aptitud para leer y escribir y sexo (1990)

df=dataframes_order_year[4]
# En este caso, se cambiaron los valores  manualmente por la estructura del archivo
df.iloc[0,4] ='unnamed4'
df.iloc[0,5] ='unnamed5'
df.iloc[0,7] ='unnamed7'
df.iloc[0,8] ='unnamed8'
df.iloc[0,10] ='unnamed10'
df.iloc[0,11] ='unnamed11'
df.iloc[0,13] ='unnamed13'
df.iloc[0,14] ='unnamed14'
df.columns=df.iloc[0]
df=df.drop(0)
df=df.reset_index(drop=True)

# Renombrar columnas
unnamed_columns=df.columns.to_list()[3:]
rename_dictionary={}
for column in unnamed_columns[:3]:
    rename_dictionary[column]=f"Población de 6 a 14 años:{df[column][0]}"
for column in unnamed_columns[3:6]:
    rename_dictionary[column]=f"Sabe leer y escribir :{df[column][0]}"
for column in unnamed_columns[6:9]:
    rename_dictionary[column]=f"No sabe leer y escribir :{df[column][0]}"
for column in unnamed_columns[9:]:
    rename_dictionary[column]=f"No especificado :{df[column][0]}"


df=df.rename(columns=rename_dictionary)
print(" Columnas renombradas correctamente!")


# Remover registros 
rows_to_drop=[0,1,2,333]
df=df.drop(rows_to_drop)


# Formatear columnas
format_columns=df.columns.to_list()[3:]
for column in format_columns:
    df[column]=df[column].astype('int')

processed_dataframes.append(['1990',df])


# Censo 1995 : ## Población de 6 a 14 años por entidad federativa y edad desplegada según aptitud para leer y escribir y sexo (1995)

df=dataframes_order_year[5]

df.iloc[0,4] ='unnamed4'
df.iloc[0,5] ='unnamed5'
df.iloc[0,7] ='unnamed7'
df.iloc[0,8] ='unnamed8'
df.iloc[0,10] ='unnamed10'
df.iloc[0,11] ='unnamed11'
df.iloc[0,13] ='unnamed13'
df.iloc[0,14] ='unnamed14'
df.columns=df.iloc[0]
df=df.drop([0,1])
df=df.reset_index(drop=True)


# Renombrar columnas
unnamed_columns=df.columns.to_list()[3:]
rename_dictionary={}
for column in unnamed_columns[:3]:
    rename_dictionary[column]=f"Población de 6 a 14 años:{df[column][0]}"
for column in unnamed_columns[3:6]:
    rename_dictionary[column]=f"Sabe leer y escribir :{df[column][0]}"
for column in unnamed_columns[6:9]:
    rename_dictionary[column]=f"No sabe leer y escribir :{df[column][0]}"
for column in unnamed_columns[9:]:
    rename_dictionary[column]=f"No especificado :{df[column][0]}"


df=df.rename(columns=rename_dictionary)
print(" Columnas renombradas correctamente!")


# Remover registros 
rows_to_drop=[0,1,2,333]
df=df.drop(rows_to_drop)


# Formatear columnas
format_columns=df.columns.to_list()[3:]
for column in format_columns:
    df[column]=df[column].astype('int')

processed_dataframes.append(['1995',df])


# Censo 2000
columns=[
    'Clave de entidad federativa',
 'Nombre de la entidad',
 'Clave de municipio o delegación',
 'Nombre del municipio o delegación',
 'Clave de localidad',
 'Nombre de la localidad',
 'Longitud',
 'Latitud',
 'Altitud',
 'Población total',
 'Población masculina',
 'Población femenina',
 'Población de 0 a 4 años',
 'Población de 5 años y más',
 'Población de 6 a 14 años',
 'Población de 12 años y más',
 'Población de 15 años y más',
 'Población de 15 a 17 años',
 'Población de 15 a 24 años',
 'Po blación femenina de 15 a 49 años',
 'Población de 18 años y más',
 'Población masculina de 18 años y más',
 'Población femenina de 18 años y más',
 'Población de 6 a 14 años que sabe leer y escribir',
 'Población de 6 a 14 años que no sabe leer y escribir',
 'Población de 15 años y más alfabeta',
 'Población de 15 años y más analfabeta',
 'Población de 5 años que asiste a la escuela',
 'Población de 5 años que no asiste a la escuela',
 'Población de 6 a 14 años que asiste a la escuela',
 'Población de 6 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población de 15 a 24 años que asiste a la escuela',
 'Población de 15 a 24 años que no asiste a la escuela',
 'Población de 15 años y más sin instrucción',
 'Población de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población de 15 años y más con instrucción posprimaria',
 'Población de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población de 15 años y más sin instrucción posprimaria',
 'Población de 15 años y más con instrucción secundaria o estudios técnicos o comerciales con primaria terminada',
 'Población de 15 años y más con instrucción media superior o superior',
 'Población de 18 años y más sin instrucción media superior',
 'Población de 18 años y más con instrucción media superior',
 'Población de 18 años y más con instrucción superior',
 'Grado promedio de escolaridad',
]

string_columns=[
 'Clave de entidad federativa',
 'Nombre de la entidad',
 'Clave de municipio o delegación',
 'Nombre del municipio o delegación',
 'Clave de localidad',
 'Nombre de la localidad',]
float_columns=[
 'Grado promedio de escolaridad','Longitud',
 'Latitud',
 'Altitud',]
integer_columns=['Población total',
 'Población masculina',
 'Población femenina',
 'Población de 0 a 4 años',
 'Población de 5 años y más',
 'Población de 6 a 14 años',
 'Población de 12 años y más',
 'Población de 15 años y más',
 'Población de 15 a 17 años',
 'Población de 15 a 24 años',
 'Po blación femenina de 15 a 49 años',
 'Población de 18 años y más',
 'Población masculina de 18 años y más',
 'Población femenina de 18 años y más',
 'Población de 6 a 14 años que sabe leer y escribir',
 'Población de 6 a 14 años que no sabe leer y escribir',
 'Población de 15 años y más alfabeta',
 'Población de 15 años y más analfabeta',
 'Población de 5 años que asiste a la escuela',
 'Población de 5 años que no asiste a la escuela',
 'Población de 6 a 14 años que asiste a la escuela',
 'Población de 6 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población de 15 a 24 años que asiste a la escuela',
 'Población de 15 a 24 años que no asiste a la escuela',
 'Población de 15 años y más sin instrucción',
 'Población de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población de 15 años y más con instrucción posprimaria',
 'Población de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población de 15 años y más sin instrucción posprimaria',
 'Población de 15 años y más con instrucción secundaria o estudios técnicos o comerciales con primaria terminada',
 'Población de 15 años y más con instrucción media superior o superior',
 'Población de 18 años y más sin instrucción media superior',
 'Población de 18 años y más con instrucción media superior',
 'Población de 18 años y más con instrucción superior',]

format_columns={
    'string_columns':string_columns,
    'float_columns':float_columns,
    'integer_columns':integer_columns
}

df=dataframes_order_year[6]
dictionary_df=diccionarios_de_datos[3]
df=filtro_columnas(df,dictionary_df,columns)
revision_nulos(df)
df=df[~(df['Grado promedio de escolaridad']=='*')] # 43 % de los registros contienen este valor
df=df[~(df['Grado promedio de escolaridad']=='N/D')] # 1% de los registros contienen  este valor
df=df[~((df['Longitud']==', LA')|((df['Longitud']==', LA (R')))] # Solo dos registros tienen este valor erroneo
formato_columnas(df,format_columns)
processed_dataframes.append(['2000',df])


# 2005 
columns=[
       'Entidad Federativa',
       'Clave del Municipio',
       'Municipio',
       'Clave de Localidad',
       'Localidad', 'Longitud', 'Latitud', 'Altitud', 
       'Población total','Población masculina', 'Población femenina',
       # Columnas relacionadas con la educacion
       'Población de 8 a 14 años que no sabe leer y escribir',
       'Población masculina de 8 a 14 años que no sabe leer y escribir',
       'Población femenina de 8 a 14 años que no sabe leer y escribir',
       'Población de 15 años y más analfabeta',
       'Población masculina de 15 años y más analfabeta',
       'Población femenina de 15 años y más analfabeta',
       'Población de 5 años que no asiste a la escuela',
       'Población masculina de 5 años que no asiste a la escuela',
       'Población femenina de 5 años que no asiste a la escuela',
       'Población de 6 a 11 años que no asiste a la escuela',
       'Población de 6 a 14 años que no asiste a la escuela',
       'Población masculina de 6 a 14 años que no asiste a la escuela',
       'Población femenina de 6 a 14 años que no asiste a la escuela',
       'Población de 12 a 14 años que no asiste a la escuela',
       'Población de 15 a 24 años que asiste a la escuela',
       'Población masculina de 15 a 24 años que asiste a la escuela',
       'Población femenina de 15 a 24 años que asiste a la escuela',
       'Población de 15 años y más sin escolaridad',
       'Población masculina de 15 años y más sin escolaridad',
       'Población femenina de 15 años y más sin escolaridad',
       'Población de 15 años y más con educación básica incompleta',
       'Población masculina de 15 años y más con educación básica incompleta',
       'Población femenina de 15 años y más con educación básica incompleta',
       'Población de 15 años y más con educación básica completa',
       'Población masculina de 15 años y más con educación básica completa',
       'Población femenina de 15 años y más con educación básica completa',
       'Población de 15 años y más con educación posbásica',
       'Población masculina de 15 años y más con educación posbásica',
       'Población femenina de 15 años y más con educación posbásica',
       'Grado promedio de escolaridad',
       'Grado promedio de escolaridad de la población masculina',
       'Grado promedio de escolaridad de la población femenina',
         ]

string_columns=[
       'Entidad Federativa',
       'Clave del Municipio',
       'Municipio',
       'Clave de Localidad',
       'Localidad',
]
float_columns=[
    'Longitud', 'Latitud', 'Altitud',
    'Grado promedio de escolaridad',
    'Grado promedio de escolaridad de la población masculina',
    'Grado promedio de escolaridad de la población femenina',

]

integer_columns=[
       'Población total','Población masculina', 'Población femenina',
       'Población de 8 a 14 años que no sabe leer y escribir',
       'Población masculina de 8 a 14 años que no sabe leer y escribir',
       'Población femenina de 8 a 14 años que no sabe leer y escribir',
       'Población de 15 años y más analfabeta',
       'Población masculina de 15 años y más analfabeta',
       'Población femenina de 15 años y más analfabeta',
       'Población de 5 años que no asiste a la escuela',
       'Población masculina de 5 años que no asiste a la escuela',
       'Población femenina de 5 años que no asiste a la escuela',
       'Población de 6 a 11 años que no asiste a la escuela',
       'Población de 6 a 14 años que no asiste a la escuela',
       'Población masculina de 6 a 14 años que no asiste a la escuela',
       'Población femenina de 6 a 14 años que no asiste a la escuela',
       'Población de 12 a 14 años que no asiste a la escuela',
       'Población de 15 a 24 años que asiste a la escuela',
       'Población masculina de 15 a 24 años que asiste a la escuela',
       'Población femenina de 15 a 24 años que asiste a la escuela',
       'Población de 15 años y más sin escolaridad',
       'Población masculina de 15 años y más sin escolaridad',
       'Población femenina de 15 años y más sin escolaridad',
       'Población de 15 años y más con educación básica incompleta',
       'Población masculina de 15 años y más con educación básica incompleta',
       'Población femenina de 15 años y más con educación básica incompleta',
       'Población de 15 años y más con educación básica completa',
       'Población masculina de 15 años y más con educación básica completa',
       'Población femenina de 15 años y más con educación básica completa',
       'Población de 15 años y más con educación posbásica',
       'Población masculina de 15 años y más con educación posbásica',
       'Población femenina de 15 años y más con educación posbásica',
    
]

format_columns={
    'string_columns':string_columns,
    'float_columns':float_columns,
    'integer_columns':integer_columns
}



df=dataframes_order_year[7]
dictionary_df=diccionarios_de_datos[0]
df=filtro_columnas(df,dictionary_df,columns)
revision_nulos(df)
df=df[~(df['Grado promedio de escolaridad']=='*')] # 43 % de los registros contienen este valor
df=df[~(df['Grado promedio de escolaridad']=='N/D')] # 1% de los registros contienen  este valor
df=df[~((df['Longitud']==', LA')|((df['Longitud']==', LA (R')))] # Solo dos registros tienen este valor erroneo
formato_columnas(df,format_columns)
processed_dataframes.append(['2005',df])


# Censo 2010
columns=[
       'Clave de entidad federativa',
 'Entidad federativa',
 'Clave de municipio ó delegación',
 'Municipio ó delegación',
 'Clave de localidad',
 'Localidad',
 'Longitud',
 'Latitud',
 'Altitud',
 'Población total',
 'Población masculina',
 'Población femenina',
 'Población de 0 a 2 años ',
 'Población masculina de 0 a 2 años',
 'Población femenina de 0 a 2 años',
 'Población de  3 años y más',
 'Población masculina de 3 años y más',
 'Población femenina de 3 años y más',
 'Población de  5 años y más',
 'Población masculina de 5 años y más',
 'Población femenina de 5 años y más',
 'Población de 12 años y más',
 'Población masculina de 12 años y más',
 'Población femenina de 12 años y más',
 'Población de 15 años y más',
 'Población masculina de 15 años y más',
 'Población femenina de 15 años y más',
 'Población de 18 años y más',
 'Población masculina de 18 años y más',
 'Población femenina de 18 años y más',
 'Población de 3 a 5 años',
 'Población masculina de 3 a 5 años',
 'Población femenina de 3 a 5 años',
 'Población de 6 a 11 años',
 'Población masculina de 6 a 11 años',
 'Población femenina de 6 a 11 años',
 'Población de 8 a 14 años',
 'Población masculina de 8 a 14 años',
 'Población femenina de 8 a 14 años',
 'Población de 12 a 14 años',
 'Población masculina de 12 a 14 años',
 'Población femenina de 12 a 14 años',
 'Población de 15 a 17 años',
 'Población masculina de 15 a 17 años',
 'Población femenina de 15 a 17 años',
 'Población de 18 a 24 años',
 'Población masculina de 18 a 24 años',
 'Población femenina de 18 a 24 años',
 'Población femenina de 15 a 49 años\xa0',
 'Población de 60 años y más',
 'Población masculina de 60 años y más',
 'Población femenina de 60 años y más',
 'Relación hombres-mujeres',
 'Población de cero a 14 años',
 'Población de 15 a 64 años',
 'Población con limitación en la actividad',
 'Población con limitación para caminar o moverse, subir o bajar',
 'Población con limitación para ver, aún usando lentes',
 'Población con limitación para hablar, comunicarse o conversar',
 'Población con limitación para escuchar',
 'Población con limitación para vestirse, bañarse o comer',
 'Población con limitación para poner atención o aprender cosas sencillas',
 'Población con limitación mental',
 'Población sin limitación en la actividad',
 'Población de 3 a 5 años que no asiste a la escuela ',
 'Población masculina de 3 a 5 años que no asiste a la escuela ',
 'Población femenina de 3 a 5 años que no asiste a la escuela ',
 'Población de 6 a 11 años que no asiste a la escuela',
 'Población masculina de 6 a 11 años que no asiste a la escuela',
 'Población femenina de 6 a 11 años que no asiste a la escuela',
 'Población de 12 a 14 años que no asiste a la escuela',
 'Población masculina de 12 a 14 años que no asiste a la escuela',
 'Población femenina de 12 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población masculina de 15 a 17 años que asiste a la escuela',
 'Población femenina de 15 a 17 años que asiste a la escuela',
 'Población de 18 a 24 años que asiste a la escuela',
 'Población masculina de 18 a 24 años que asiste a la escuela',
 'Población femenina de 18 a 24 años que asiste a la escuela',
 'Población de 8 a 14 años que no saben leer y escribir',
 'Población masculina de 8 a 14 años que no saben leer y escribir',
 'Población femenina  de 8 a 14 años que no saben leer y escribir',
 'Población de 15 años y más analfabeta',
 'Población masculina de 15 años y más analfabeta',
 'Población femenina de 15 años y más analfabeta',
 'Población de 15 años y más sin escolaridad',
 'Población masculina de 15 años y más sin escolaridad',
 'Población femenina de 15 años y más sin escolaridad',
 'Población de 15 años y más con primaria incompleta',
 'Población masculina de 15 años y más con primaria incompleta',
 'Población femenina de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población masculina de 15 años y más con primaria completa',
 'Población femenina de 15 años y más con primaria completa',
 'Población de 15 años y más con secundaria incompleta',
 'Población masculina de 15 años y más con secundaria incompleta',
 'Población femenina de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población masculina de 15 años y más con secundaria completa',
 'Población femenina de 15 años y más con secundaria completa',
 'Población de 18 años y más con educación pos-básica',
 'Población masculina de 18 años y más con educación pos-básica',
 'Población femenina de 18 años y más con educación pos-básica',
 'Grado promedio de escolaridad',
 'Grado promedio de escolaridad de la población masculina',
 'Grado promedio de escolaridad de la población femenina',
       
         ]

string_columns=[
    'Clave de entidad federativa',
 'Entidad federativa',
 'Clave de municipio ó delegación',
 'Municipio ó delegación',
 'Clave de localidad',
 'Localidad',
     
]
float_columns=[
 'Longitud',
 'Latitud',
 'Altitud',
 'Grado promedio de escolaridad',
 'Grado promedio de escolaridad de la población masculina',
 'Grado promedio de escolaridad de la población femenina',
    
    

]

integer_columns=[
     'Población total',
 'Población masculina',
 'Población femenina',
 'Población de 0 a 2 años ',
 'Población masculina de 0 a 2 años',
 'Población femenina de 0 a 2 años',
 'Población de  3 años y más',
 'Población masculina de 3 años y más',
 'Población femenina de 3 años y más',
 'Población de  5 años y más',
 'Población masculina de 5 años y más',
 'Población femenina de 5 años y más',
 'Población de 12 años y más',
 'Población masculina de 12 años y más',
 'Población femenina de 12 años y más',
 'Población de 15 años y más',
 'Población masculina de 15 años y más',
 'Población femenina de 15 años y más',
 'Población de 18 años y más',
 'Población masculina de 18 años y más',
 'Población femenina de 18 años y más',
 'Población de 3 a 5 años',
 'Población masculina de 3 a 5 años',
 'Población femenina de 3 a 5 años',
 'Población de 6 a 11 años',
 'Población masculina de 6 a 11 años',
 'Población femenina de 6 a 11 años',
 'Población de 8 a 14 años',
 'Población masculina de 8 a 14 años',
 'Población femenina de 8 a 14 años',
 'Población de 12 a 14 años',
 'Población masculina de 12 a 14 años',
 'Población femenina de 12 a 14 años',
 'Población de 15 a 17 años',
 'Población masculina de 15 a 17 años',
 'Población femenina de 15 a 17 años',
 'Población de 18 a 24 años',
 'Población masculina de 18 a 24 años',
 'Población femenina de 18 a 24 años',
 'Población femenina de 15 a 49 años\xa0',
 'Población de 60 años y más',
 'Población masculina de 60 años y más',
 'Población femenina de 60 años y más',
 'Relación hombres-mujeres',
 'Población de cero a 14 años',
 'Población de 15 a 64 años',
 'Población con limitación en la actividad',
 'Población con limitación para caminar o moverse, subir o bajar',
 'Población con limitación para ver, aún usando lentes',
 'Población con limitación para hablar, comunicarse o conversar',
 'Población con limitación para escuchar',
 'Población con limitación para vestirse, bañarse o comer',
 'Población con limitación para poner atención o aprender cosas sencillas',
 'Población con limitación mental',
 'Población sin limitación en la actividad',
 'Población de 3 a 5 años que no asiste a la escuela ',
 'Población masculina de 3 a 5 años que no asiste a la escuela ',
 'Población femenina de 3 a 5 años que no asiste a la escuela ',
 'Población de 6 a 11 años que no asiste a la escuela',
 'Población masculina de 6 a 11 años que no asiste a la escuela',
 'Población femenina de 6 a 11 años que no asiste a la escuela',
 'Población de 12 a 14 años que no asiste a la escuela',
 'Población masculina de 12 a 14 años que no asiste a la escuela',
 'Población femenina de 12 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población masculina de 15 a 17 años que asiste a la escuela',
 'Población femenina de 15 a 17 años que asiste a la escuela',
 'Población de 18 a 24 años que asiste a la escuela',
 'Población masculina de 18 a 24 años que asiste a la escuela',
 'Población femenina de 18 a 24 años que asiste a la escuela',
 'Población de 8 a 14 años que no saben leer y escribir',
 'Población masculina de 8 a 14 años que no saben leer y escribir',
 'Población femenina  de 8 a 14 años que no saben leer y escribir',
 'Población de 15 años y más analfabeta',
 'Población masculina de 15 años y más analfabeta',
 'Población femenina de 15 años y más analfabeta',
 'Población de 15 años y más sin escolaridad',
 'Población masculina de 15 años y más sin escolaridad',
 'Población femenina de 15 años y más sin escolaridad',
 'Población de 15 años y más con primaria incompleta',
 'Población masculina de 15 años y más con primaria incompleta',
 'Población femenina de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población masculina de 15 años y más con primaria completa',
 'Población femenina de 15 años y más con primaria completa',
 'Población de 15 años y más con secundaria incompleta',
 'Población masculina de 15 años y más con secundaria incompleta',
 'Población femenina de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población masculina de 15 años y más con secundaria completa',
 'Población femenina de 15 años y más con secundaria completa',
 'Población de 18 años y más con educación pos-básica',
 'Población masculina de 18 años y más con educación pos-básica',
 'Población femenina de 18 años y más con educación pos-básica',
]

format_columns={
    'string_columns':string_columns,
    'float_columns':float_columns,
    'integer_columns':integer_columns
}

df=dataframes_order_year[8]
dictionary_df=diccionarios_de_datos[2]

dictionary_df['mnemonico'][1]='nom_ent'
dictionary_df['mnemonico'][3]='nom_mun'
dictionary_df['mnemonico'][5]='nom_loc'
dictionary_df['mnemonico'][6]='longitud'
dictionary_df['mnemonico'][18]='p_5ymas'
dictionary_df['mnemonico'][100]='p15a17a'
dictionary_df['mnemonico'][103]='p18a24a'
dictionary_df['mnemonico'][131]='graproes_m'
dictionary_df['mnemonico'][146]='pder_ss'
dictionary_df['mnemonico'][147]='pder_imss'
dictionary_df['mnemonico'][180]='vph_3ymasc'
dictionary_df['mnemonico'][195]='vph_pc'

df=filtro_columnas(df,dictionary_df,columns)
revision_nulos(df)
df=df[~(df['Grado promedio de escolaridad']=='*')] # 43 % de los registros contienen este valor
df=df[~(df['Grado promedio de escolaridad']=='N/D')] # 1% de los registros contienen  este valor
df=df[~((df['Longitud']==', LA')|((df['Longitud']==', LA (R')))] # Solo dos registros tienen este valor erroneo
formato_columnas(df,format_columns)
processed_dataframes.append(['2010',df])


# Censo 2020
columns=[
    'Clave de entidad federativa',
 'Entidad federativa',
 'Clave de municipio o demarcación territorial',
 'Municipio o demarcación territorial',
 'Clave de localidad',
 'Localidad',
 'Longitud',
 'Latitud',
 'Altitud',
 'Población total',
 'Población femenina',
 'Población masculina',
 'Población de 0 a 2 años',
 'Población femenina de 0 a 2 años',
 'Población masculina de 0 a 2 años',
 'Población de 3 años y más',
 'Población femenina de 3 años y más',
 'Población masculina de 3 años y más',
 'Población de 5 años y más',
 'Población femenina de 5 años y más',
 'Población masculina de 5 años y más',
 'Población de 12 años y más',
 'Población femenina de 12 años y más',
 'Población masculina de 12 años y más',
 'Población de 15 años y más',
 'Población femenina de 15 años y más',
 'Población masculina de 15 años y más',
 'Población de 18 años y más',
 'Población femenina de 18 años y más',
 'Población masculina de 18 años y más',
 'Población de 3 a 5 años',
 'Población femenina de 3 a 5 años',
 'Población masculina de 3 a 5 años',
 'Población de 6 a 11 años',
 'Población femenina de 6 a 11 años',
 'Población masculina de 6 a 11 años',
 'Población de 8 a 14 años',
 'Población femenina de 8 a 14 años',
 'Población masculina de 8 a 14 años',
 'Población de 12 a 14 años',
 'Población femenina de 12 a 14 años',
 'Población masculina de 12 a 14 años',
 'Población de 15 a 17 años',
 'Población femenina de 15 a 17 años',
 'Población masculina de 15 a 17 años',
 'Población de 18 a 24 años',
 'Población femenina de 18 a 24 años',
 'Población masculina de 18 a 24 años',
 'Población femenina de 15 a 49 años',
 'Población de 60 años y más',
 'Población femenina de 60 años y más',
 'Población masculina de 60 años y más',
 'Relación hombres-mujeres',
 'Población de 0 a 14 años',
 'Población de 15 a 64 años',
 'Población de 65 años y más',
 'Población de 0 a 4 años',
 'Población femenina de 0 a 4 años',
 'Población masculina de 0 a 4 años',
 'Población de 5 a 9 años',
 'Población femenina de 5 a 9 años',
 'Población masculina de 5 a 9 años',
 'Población de 10 a 14 años',
 'Población femenina de 10 a 14 años',
 'Población masculina de 10 a 14 años',
 'Población de 15 a 19 años',
 'Población femenina de 15 a 19 años',
 'Población masculina de 15 a 19 años',
 'Población de 20 a 24 años',
 'Población femenina de 20 a 24 años',
 'Población masculina de 20 a 24 años',
 'Población de 25 a 29 años',
 'Población femenina de 25 a 29 años',
 'Población masculina de 25 a 29 años',
 'Población de 30 a 34 años',
 'Población femenina de 30 a 34 años',
 'Población masculina de 30 a 34 años',
 'Población de 35 a 39 años',
 'Población femenina de 35 a 39 años',
 'Población masculina de 35 a 39 años',
 'Población de 40 a 44 años',
 'Población femenina de 40 a 44 años',
 'Población masculina de 40 a 44 años',
 'Población de 45 a 49 años',
 'Población femenina de 45 a 49 años',
 'Población masculina de 45 a 49 años',
 'Población de 50 a 54 años',
 'Población femenina de 50 a 54 años',
 'Población masculina de 50 a 54 años',
 'Población de 55 a 59 años',
 'Población femenina de 55 a 59 años',
 'Población masculina de 55 a 59 años',
 'Población de 60 a 64 años',
 'Población femenina de 60 a 64 años',
 'Población masculina de 60 a 64 años',
 'Población de 65 a 69 años',
 'Población femenina de 65 a 69 años',
 'Población masculina de 65 a 69 años',
 'Población de 70 a 74 años',
 'Población femenina de 70 a 74 años',
 'Población masculina de 70 a 74 años',
 'Población de 75 a 79 años',



 'Población con discapacidad',
 'Población con discapacidad para hablar o comunicarse',
 'Población con discapacidad para oír, aun usando aparato auditivo',
 'Población con discapacidad para vestirse, bañarse o comer',
 'Población con discapacidad para recordar o concentrarse',
 'Población con limitación',
 'Población con limitación para caminar, subir o bajar',
 'Población con limitación para ver, aun usando lentes',
 'Población con limitación para hablar o comunicarse',
 'Población con limitación para oír, aun usando aparato auditivo',
 'Población con limitación para vestirse, bañarse o comer',
 'Población con limitación para recordar o concentrarse',
 'Población con algún problema o condición mental',
 'Población sin discapacidad, limitación, problema o condición mental',
 'Población de 3 a 5 años que no asiste a la escuela',
 'Población femenina de 3 a 5 años que no asiste a la escuela',
 'Población masculina de 3 a 5 años que no asiste a la escuela',
 'Población de 6 a 11 años que no asiste a la escuela',
 'Población femenina de 6 a 11 años que no asiste a la escuela',
 'Población masculina de 6 a 11 años que no asiste a la escuela',
 'Población de 12 a 14 años que no asiste a la escuela',
 'Población femenina de 12 a 14 años que no asiste a la escuela',
 'Población masculina de 12 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población femenina de 15 a 17 años que asiste a la escuela',
 'Población masculina de 15 a 17 años que asiste a la escuela',
 'Población de 18 a 24 años que asiste a la escuela',
 'Población femenina de 18 a 24 años que asiste a la escuela',
 'Población masculina de 18 a 24 años que asiste a la escuela',
 'Población de 8 a 14 años que no sabe leer y escribir',
 'Población femenina de 8 a 14 años que no sabe leer y escribir',
 'Población masculina de 8 a 14 años que no sabe leer y escribir',
 'Población de 15 años y más analfabeta',
 'Población femenina de 15 años y más analfabeta',
 'Población masculina de 15 años y más analfabeta',
 'Población de 15 años y más sin escolaridad',
 'Población femenina de 15 años y más sin escolaridad',
 'Población masculina de 15 años y más sin escolaridad',
 'Población de 15 años y más con primaria incompleta',
 'Población femenina de 15 años y más con primaria incompleta',
 'Población masculina de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población femenina de 15 años y más con primaria completa',
 'Población masculina de 15 años y más con primaria completa',
 'Población de 15 años y más con secundaria incompleta',
 'Población femenina de 15 años y más con secundaria incompleta',
 'Población masculina de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población femenina de 15 años y más con secundaria completa',
 'Población masculina de 15 años y más con secundaria completa',
 'Población de 18 años y más con educación posbásica',
 'Población femenina de 18 años y más con educación posbásica',
 'Población masculina de 18 años y más con educación posbásica',
 'Grado promedio de escolaridad',
 'Grado promedio de escolaridad de la población femenina',
 'Grado promedio de escolaridad de la población masculina',
 'Población de 12 años y más económicamente activa',
 'Población femenina de 12 años y más económicamente activa',
 'Población masculina de 12 años y más económicamente activa',
 'Población de 12 años y más no económicamente activa',
 'Población femenina de 12 años y más no económicamente activa',
 'Población masculina de 12 años y más no económicamente activa',
 'Población de 12 años y más ocupada',
 'Población femenina de 12 años y más ocupada',
 'Población masculina de 12 años y más ocupada',
 'Población de 12 años y más desocupada',
 'Población femenina de 12 años y más desocupada',
 'Población masculina de 12 años y más desocupada',
 

 
       
         ]

string_columns=[
    'Clave de entidad federativa',
 'Entidad federativa',
 'Clave de municipio o demarcación territorial',
 'Municipio o demarcación territorial',
 'Clave de localidad',
 'Localidad',
    
     
]
float_columns=[
    'Longitud',
 'Latitud',
 'Altitud',
    'Relación hombres-mujeres',
    'Grado promedio de escolaridad',
 'Grado promedio de escolaridad de la población femenina',
 'Grado promedio de escolaridad de la población masculina'

    

]

integer_columns=[
    'Población total',
 'Población femenina',
 'Población masculina',
 'Población de 0 a 2 años',
 'Población femenina de 0 a 2 años',
 'Población masculina de 0 a 2 años',
 'Población de 3 años y más',
 'Población femenina de 3 años y más',
 'Población masculina de 3 años y más',
 'Población de 5 años y más',
 'Población femenina de 5 años y más',
 'Población masculina de 5 años y más',
 'Población de 12 años y más',
 'Población femenina de 12 años y más',
 'Población masculina de 12 años y más',
 'Población de 15 años y más',
 'Población femenina de 15 años y más',
 'Población masculina de 15 años y más',
 'Población de 18 años y más',
 'Población femenina de 18 años y más',
 'Población masculina de 18 años y más',
 'Población de 3 a 5 años',
 'Población femenina de 3 a 5 años',
 'Población masculina de 3 a 5 años',
 'Población de 6 a 11 años',
 'Población femenina de 6 a 11 años',
 'Población masculina de 6 a 11 años',
 'Población de 8 a 14 años',
 'Población femenina de 8 a 14 años',
 'Población masculina de 8 a 14 años',
 'Población de 12 a 14 años',
 'Población femenina de 12 a 14 años',
 'Población masculina de 12 a 14 años',
 'Población de 15 a 17 años',
 'Población femenina de 15 a 17 años',
 'Población masculina de 15 a 17 años',
 'Población de 18 a 24 años',
 'Población femenina de 18 a 24 años',
 'Población masculina de 18 a 24 años',
 'Población femenina de 15 a 49 años',
 'Población de 60 años y más',
 'Población femenina de 60 años y más',
 'Población masculina de 60 años y más',
 
 'Población de 0 a 14 años',
 'Población de 15 a 64 años',
 'Población de 65 años y más',
 'Población de 0 a 4 años',
 'Población femenina de 0 a 4 años',
 'Población masculina de 0 a 4 años',
 'Población de 5 a 9 años',
 'Población femenina de 5 a 9 años',
 'Población masculina de 5 a 9 años',
 'Población de 10 a 14 años',
 'Población femenina de 10 a 14 años',
 'Población masculina de 10 a 14 años',
 'Población de 15 a 19 años',
 'Población femenina de 15 a 19 años',
 'Población masculina de 15 a 19 años',
 'Población de 20 a 24 años',
 'Población femenina de 20 a 24 años',
 'Población masculina de 20 a 24 años',
 'Población de 25 a 29 años',
 'Población femenina de 25 a 29 años',
 'Población masculina de 25 a 29 años',
 'Población de 30 a 34 años',
 'Población femenina de 30 a 34 años',
 'Población masculina de 30 a 34 años',
 'Población de 35 a 39 años',
 'Población femenina de 35 a 39 años',
 'Población masculina de 35 a 39 años',
 'Población de 40 a 44 años',
 'Población femenina de 40 a 44 años',
 'Población masculina de 40 a 44 años',
 'Población de 45 a 49 años',
 'Población femenina de 45 a 49 años',
 'Población masculina de 45 a 49 años',
 'Población de 50 a 54 años',
 'Población femenina de 50 a 54 años',
 'Población masculina de 50 a 54 años',
 'Población de 55 a 59 años',
 'Población femenina de 55 a 59 años',
 'Población masculina de 55 a 59 años',
 'Población de 60 a 64 años',
 'Población femenina de 60 a 64 años',
 'Población masculina de 60 a 64 años',
 'Población de 65 a 69 años',
 'Población femenina de 65 a 69 años',
 'Población masculina de 65 a 69 años',
 'Población de 70 a 74 años',
 'Población femenina de 70 a 74 años',
 'Población masculina de 70 a 74 años',
 'Población de 75 a 79 años',
 'Población con discapacidad',
 'Población con discapacidad para hablar o comunicarse',
 'Población con discapacidad para oír, aun usando aparato auditivo',
 'Población con discapacidad para vestirse, bañarse o comer',
 'Población con discapacidad para recordar o concentrarse',
 'Población con limitación',
 'Población con limitación para caminar, subir o bajar',
 'Población con limitación para ver, aun usando lentes',
 'Población con limitación para hablar o comunicarse',
 'Población con limitación para oír, aun usando aparato auditivo',
 'Población con limitación para vestirse, bañarse o comer',
 'Población con limitación para recordar o concentrarse',
 'Población con algún problema o condición mental',
 'Población sin discapacidad, limitación, problema o condición mental',
 'Población de 3 a 5 años que no asiste a la escuela',
 'Población femenina de 3 a 5 años que no asiste a la escuela',
 'Población masculina de 3 a 5 años que no asiste a la escuela',
 'Población de 6 a 11 años que no asiste a la escuela',
 'Población femenina de 6 a 11 años que no asiste a la escuela',
 'Población masculina de 6 a 11 años que no asiste a la escuela',
 'Población de 12 a 14 años que no asiste a la escuela',
 'Población femenina de 12 a 14 años que no asiste a la escuela',
 'Población masculina de 12 a 14 años que no asiste a la escuela',
 'Población de 15 a 17 años que asiste a la escuela',
 'Población femenina de 15 a 17 años que asiste a la escuela',
 'Población masculina de 15 a 17 años que asiste a la escuela',
 'Población de 18 a 24 años que asiste a la escuela',
 'Población femenina de 18 a 24 años que asiste a la escuela',
 'Población masculina de 18 a 24 años que asiste a la escuela',
 'Población de 8 a 14 años que no sabe leer y escribir',
 'Población femenina de 8 a 14 años que no sabe leer y escribir',
 'Población masculina de 8 a 14 años que no sabe leer y escribir',
 'Población de 15 años y más analfabeta',
 'Población femenina de 15 años y más analfabeta',
 'Población masculina de 15 años y más analfabeta',
 'Población de 15 años y más sin escolaridad',
 'Población femenina de 15 años y más sin escolaridad',
 'Población masculina de 15 años y más sin escolaridad',
 'Población de 15 años y más con primaria incompleta',
 'Población femenina de 15 años y más con primaria incompleta',
 'Población masculina de 15 años y más con primaria incompleta',
 'Población de 15 años y más con primaria completa',
 'Población femenina de 15 años y más con primaria completa',
 'Población masculina de 15 años y más con primaria completa',
 'Población de 15 años y más con secundaria incompleta',
 'Población femenina de 15 años y más con secundaria incompleta',
 'Población masculina de 15 años y más con secundaria incompleta',
 'Población de 15 años y más con secundaria completa',
 'Población femenina de 15 años y más con secundaria completa',
 'Población masculina de 15 años y más con secundaria completa',
 'Población de 18 años y más con educación posbásica',
 'Población femenina de 18 años y más con educación posbásica',
 'Población masculina de 18 años y más con educación posbásica',
 'Población de 12 años y más económicamente activa',
 'Población femenina de 12 años y más económicamente activa',
 'Población masculina de 12 años y más económicamente activa',
 'Población de 12 años y más no económicamente activa',
 'Población femenina de 12 años y más no económicamente activa',
 'Población masculina de 12 años y más no económicamente activa',
 'Población de 12 años y más ocupada',
 'Población femenina de 12 años y más ocupada',
 'Población masculina de 12 años y más ocupada',
 'Población de 12 años y más desocupada',
 'Población femenina de 12 años y más desocupada',
 'Población masculina de 12 años y más desocupada',
]

format_columns={
    'string_columns':string_columns,
    'float_columns':float_columns,
    'integer_columns':integer_columns
}


df=dataframes_order_year[9]
dictionary_df=diccionarios_de_datos[1]

# Proceso feo de renombramiento de columnas
# %----------------------------------------------------------------------%%
def fix_encoding(text):
    return text.encode('latin1').decode('utf-8')

rename_columns=dictionary_df.columns.to_list()[:5]
for column in rename_columns:
    dictionary_df[column]=dictionary_df[column].astype('str')
    dictionary_df[column]=dictionary_df[column].apply(fix_encoding)
dictionary_df=dictionary_df.drop([0,1,2])
dictionary_df=dictionary_df.reset_index(drop=True)


dictionary_df.columns=dictionary_df.loc[0]

dictionary_df=dictionary_df.drop(0)
dictionary_df=dictionary_df.reset_index(drop=True)
dictionary_df=dictionary_df[dictionary_df.columns.to_list()[:6]]

dictionary_df['Mnemónico'][1]='NOM_ENT'
dictionary_df['Mnemónico'][3]='NOM_MUN'
dictionary_df['Mnemónico'][5]='NOM_LOC'
dictionary_df['Mnemónico'][6]='LONGITUD'
dictionary_df['Indicador'][48]='Población femenina de 15 a 49 años'

rename_dictionary={}
for index,row in dictionary_df.iterrows():
        old_column_name=row['Mnemónico']
        new_column_name=row['Indicador']
        rename_dictionary[old_column_name] = new_column_name

df=df.rename(columns=rename_dictionary)
df=df[columns]

# %%----------------------------------------------------------------------%

revision_nulos(df)
df=df[~(df['Grado promedio de escolaridad']=='*')] # 43 % de los registros contienen este valor
df=df[~(df['Grado promedio de escolaridad']=='N/D')] # menos de 0.1% de los registros contienen  este valor
df=df[~(df['Longitud']=='102°17\\')] # menos de 0.1% de los registros contienen  este valor
df=df[~(df['Latitud']=='21°52\\')] # menos de 0.1% de los registros contienen  este valor
df=df[~(df['Altitud']=='00-1')] # menos de 0.1% de los registros contienen  este valor


df=df[~((df['Longitud']==', LA')|((df['Longitud']==', LA (R')))] # Solo dos registros tienen este valor erroneo
formato_columnas(df,format_columns)
processed_dataframes.append(['2020',df])

for df in processed_dataframes:
    file_path=f"{{{{ cookiecutter.project_slug }}}}/Data/processed/{df[0]}.csv"
    df[1].to_csv(file_path)