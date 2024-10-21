import os
import requests
import zipfile
from io import BytesIO
from datetime import datetime
import subprocess

data_path="data/raw/DATOS EDUCACION"

if not(os.path.exists(data_path)):
    print(f"Creando {data_path} ...")

os.makedirs(data_path,exist_ok=True)

def nombre_archivo(url):
    """
    url:URL de descarga del archivo que se quiere extraer el nombre

    Esta función recibe el  url de un archivo, y arroja el nombre del archivo con y sin el tipo de formato en el que esta guardado.
    """
    # Nombre con el tipo de formato incluido
    indices=[index for index in range(len(url)) if url[index]=="/"]
    last_slash=indices[-1]
    file_name_with=url[last_slash+1:]

    # Nombre sin el tipo de formato incluido
    indices=[index for index in range(len(file_name_with)) if file_name_with[index]=="."]
    last_point=indices[-1]
    file_name_without=file_name_with[last_point+1:]

    return {'with':file_name_with,'without':file_name_without}

def formato_de_archivo(url):
    """
    url:URL de descarga del archivo que se quiere extraer el formato en el que esta guardado

    Esta función recibe el  url de un archivo, y arroja el nombre del tipo de formato en el que esta guardado.
    """
    file_name=nombre_archivo(url)['with']
    indices=[index for index in range(len(file_name)) if file_name[index]=="."]
    last_point=indices[-1]
    return file_name[last_point+1:]

def descargar_archivo_zip(url,file_name="",folder=""):
    """ 
    url: URL de descarga
    folder: El nombre de la carpeta en donde se guardaran los datos descargados
    file_name: Nombre del archivo extraído

    Esta función 
    """
    # Creamos el directorio de extracción en caso de no existir
    
    extract_to=f"{data_path}/{folder}/{file_name}"

    os.makedirs(extract_to, exist_ok=True)

    # Descargamos el archivo zip
    response = requests.get(url)
    if response.status_code == 200:
        # Abrimos y extraemos el contenido
        with zipfile.ZipFile(BytesIO(response.content)) as z:
            z.extractall(extract_to)
            print(f'Archivo guardado {file_name}')
    else:
        print(f'Error al descargar {url}, status code: {response.status_code}')

def descargar_archivo_xlsx(url,file_name,folder=""):
    """ 
    url: URL de descarga
    folder: El nombre de la carpeta en donde se guardaran los datos descargados
    file_name: Nombre del archivo extraído
    """
    download_path=f"{data_path}/{folder}"
    # Creamos el directorio de extracción en caso de no existir
    os.makedirs(download_path, exist_ok=True)
    # Se hace una petición GET al url
    response = requests.get(url)
    

    if response.status_code == 200:
        
        file_path=f"{download_path}/{file_name}"
        # Se guarda el contenido
        with open(file_path, 'wb') as f:
            f.write(response.content)
        #print(f'Descarga completa:{url}')
        print(f'Archivo guardado:{file_name}')
    else:
        print('Error al intentar descargar el archivo, status code:', response.status_code)



#Enlaces de Censos de Población:

ccpv_siglo_XX= [
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1950/tabulados/cgp50_nal_educacion.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "cgp50_nal_educacion.xlsx"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1960/tabulados/CGP60_nal_Educacion.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "CGP60_nal_Educacion.xlsx"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1970/tabulados/cgp70_nal_educacion.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "cgp70_nal_educacion.xlsx"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1980/tabulados/cpyv80_nal_educacion.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "cpyv80_nal_educacion.xlsx"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1990/tabulados/CPyV90_Nal_Caracteristicas_educativas.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "CPyV90_Nal_Caracteristicas_educativas.xlsx"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/1995/tabulados/Cont95Enum_NAL_Caracteristicas_educativas.xlsx",
            "data": "REFUT1MgU0lHTE8gWFg=",
            "file_name": "Cont95Enum_NAL_Caracteristicas_educativas.xlsx"
        }
        
       
   
]

ccpv_siglo_XXI= [
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2000/datosabiertos/cgpv2000_iter_00_csv.zip",
            "data": "REFUT1MgU0lHTE8gWFhJ",
            "file_name": "cgpv2000_iter_00"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2005/datosabiertos/cpv2005_iter_00_csv.zip",
            "data": "REFUT1MgU0lHTE8gWFhJ",
            "file_name": "cpv2005_iter_00"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2010/datosabiertos/iter_nal_2010_csv.zip",
            "data": "REFUT1MgU0lHTE8gWFhJ",
            "file_name": "iter_00_cpv2010"
        },
        {
            "url": "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_00_cpv2020_csv.zip",
            "data": "REFUT1MgU0lHTE8gWFhJ",
            "file_name": "iter_00_cpv2020"
        }
    ]


print("Empezando descarga de Censos de Población...")

# Descargar datos del censo del siglo XX
for item in ccpv_siglo_XX:
    folder="CENSOS DE POBLACION Y VIVIENDA"# Configurar

    folder_path=f"{data_path}/{folder}"
    descargar_archivo_xlsx(item["url"], item["file_name"], folder)
    download_date = datetime.now().strftime("%Y-%m-%d")
    format=formato_de_archivo(item["url"])
    size=os.path.getsize(f"{folder_path}/{item['file_name']}")
    string=f"""
           Nombre:{item['file_name']}\n
           Fecha de descarga:{download_date}\n
           Formato:{format}\n
           Tamaño:{size}\n
           URL descarga:{item['url']}\n\n

           """
    os.makedirs(f"{data_path}/descriptions/{folder}", exist_ok=True)
    with open(f"{data_path}/descriptions/{folder}/{item['file_name']}_details.txt",'w') as file:
        file.write(string)


# Descargar datos del censo del siglo XXI
for item in ccpv_siglo_XXI:
    folder="CENSOS DE POBLACION Y VIVIENDA"
    descargar_archivo_zip(item["url"], file_name="",folder=folder)
    download_date = datetime.now().strftime("%Y-%m-%d")
    format=formato_de_archivo(item["url"])
    size=os.path.getsize(f"{folder_path}/{item['file_name']}")
    string=f"""
           Nombre:{item['file_name']}\n
           Fecha de descarga:{download_date}\n
           Formato:{format}\n
           Tamaño:{size}\n
           URL descarga:{item['url']}\n\n

           """
    os.makedirs(f"{data_path}/descriptions/{folder}", exist_ok=True)
    with open(f"{data_path}/descriptions/{folder}/{item['file_name']}_details.txt",'w') as file:
        file.write(string)

print("%\%","-"*80,"%\%")
print("Contenido de Censos descargado !")
print("%\%","-"*80,"%\%")

# Encuesta Nacional Sobre Acceso y Permanencia en la Educación 2021
enape_2021=[

        {
            "url": "https://www.inegi.org.mx/contenidos/programas/enape/2021/datosabiertos/conjunto_de_datos_enape_2021_csv.zip",
            "data": "RU5DVUVTVEEgTkFDSU9OQUwgU09CUkUgQUNDRVNPIFkgUEVSTUFORU5DSUEgRU4gTEEgRURVQ0FDSU9OIDIwMjE=",
            "file_name": "conjunto_de_datos_enape_2021"
        }
        
    ]


print("Empezando descarga de datos de ENAPE 2021...")

# Descargar datos del ENAPE

for item in enape_2021:
    folder="ENCUESTA NACIONAL SOBRE ACCESO Y PERMANENCIA EN LA EDUCACION 2021"
    folder_path=f"{data_path}/{folder}"
    descargar_archivo_zip(item["url"],file_name=item['file_name'],folder=folder)
    download_date = datetime.now().strftime("%Y-%m-%d")
    format=formato_de_archivo(item["url"])
    size=os.path.getsize(f"{folder_path}/{item['file_name']}")
    string=f"""
           Nombre:{item['file_name']}\n
           Fecha de descarga:{download_date}\n
           Formato:{format}\n
           Tamaño:{size}\n
           URL descarga:{item['url']}\n\n

           """
    os.makedirs(f"{data_path}/descriptions/{folder}", exist_ok=True)
    with open(f"{data_path}/descriptions/{folder}/{item['file_name']}_details.txt",'w') as file:
        file.write(string)        

print("%\%","-"*80,"%\%")
print("Contenido de ENAPE 2021 descargado !")
print("%\%","-"*80,"%\%")

# Enlace de reporte SEP indicadores educativos 2023
sep_2023=[
        {
            "url": "https://www.planeacion.sep.gob.mx/Doc/estadistica_e_indicadores/indicadores/reporte_indicadores_educativos_sep_2023.xls",
            "data": "UkVQT1JURSBERSBJTkRJQ0FET1JFUyBFRFVDQVRJVk9T",
            "file_name": "reporte_indicadores_educativos_sep_2023.xls"
        }
    ]
# Descarga reporte del SEP 2023
# Hubo un problema con la descarga normal, entonces se descargaron los datos con el shell
command = (
    'cd "{{ cookiecutter.project_slug }}/Data/raw/DATOS EDUCACION" && '
    'mkdir "REPORTE DE INDICADORES EDUCATIVOS" && '
    'cd "REPORTE DE INDICADORES EDUCATIVOS" && '
    'curl -O https://www.planeacion.sep.gob.mx/Doc/estadistica_e_indicadores/indicadores/reporte_indicadores_educativos_sep_2023.xls'
)

print("Empezando descarga de reporte SEP 2023...")


execute=subprocess.run(command,shell=True,capture_output=True,text=True)
print(execute.stdout)
print(execute.stderr)


print("%\%","-"*80,"%\%")
print("Contenido de reporte SEP 2023 descargado !")
print("%\%","-"*80,"%\%")