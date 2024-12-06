import pandas as pd
import os
import geopandas as gpd

# Cargar los archivos proporcionados
file_data = os.path.join('..', 'data', 'raw', 'DATOS EDUCACION', 'ENCUESTA NACIONAL SOBRE ACCESO Y PERMANENCIA EN LA EDUCACION 2021',
                         'conjunto_de_datos_enape_2021', 'conjunto_de_datos_tmodulo_enape_2021', 'conjunto_de_datos',
                         'conjunto_de_datos_tmodulo_enape_2021.csv')

file_dict = os.path.join('..', 'data', 'raw', 'DATOS EDUCACION', 'ENCUESTA NACIONAL SOBRE ACCESO Y PERMANENCIA EN LA EDUCACION 2021',
                         'conjunto_de_datos_enape_2021', 'conjunto_de_datos_tmodulo_enape_2021', 'diccionario_de_datos',
                         'diccionario_datos_tmodulo_enape_2021.csv')
# Leer los archivos
data = pd.read_csv(file_data)
data_dict = pd.read_csv(file_dict)

nuevos_nombres = [
    "folio",
    "personas_vivienda",
    "hombres_vivienda",
    "mujeres_vivienda",
    "personas_0_29",
    "compu_escritorio",
    "compu_portatil",
    "tv_digital",
    "tablet_disponible",
    "celular_smartphone",
    "internet_fijo",
    "razon_no_internet",
    "escolaridad_mejora",
    "educacion_empleo",
    "educacion_decisiones",
    "entidad",
    "factor_expansion"
]

# Asignar los nuevos nombres a las columnas
data.columns = nuevos_nombres

# Identificar columnas numéricas y categóricas
numeric_columns = data.select_dtypes(include=['number']).columns
categorical_columns = data.select_dtypes(exclude=['number']).columns

# Rellenar valores faltantes
# Para columnas numéricas, usar la media
for col in numeric_columns:
    data[col] = data[col].fillna(data[col].mean())

# Para columnas categóricas, usar la moda
for col in categorical_columns:
    data[col] = data[col].fillna(data[col].mode()[0] if not data[col].mode().empty else None)

# Guardar el archivo actualizado
ruta = "../data/interim/vivienda"
os.makedirs(ruta, exist_ok=True)  # exist_ok=True evita error si la carpeta ya existe

output_path = os.path.join('..', 'data', 'interim', 'vivienda', 'dataset_vivienda_enape_2021.cleaned.csv')
data.to_csv(output_path, index=False)

file_data = os.path.join('..', 'data', 'interim', 'vivienda', 'dataset_vivienda_enape_2021.cleaned.csv')

data_cleaned = pd.read_csv(file_data)

# Generar nuevas columnas cualitativas basadas en las columnas numéricas

# 1. Clasificación por tamaño de la vivienda (pequeña, mediana, grande)
def clasificar_tamano(personas):
    if personas <= 2:
        return 'Pequeña'
    elif 3 <= personas <= 5:
        return 'Mediana'
    else:
        return 'Grande'

data_cleaned['tamano_vivienda'] = data_cleaned['personas_vivienda'].apply(clasificar_tamano)

# 2. Disponibilidad de tecnologías (Alta, Media, Baja)
def clasificar_tecnologia(row):
    tecnologias = ['compu_escritorio', 'compu_portatil', 'tv_digital', 'tablet_disponible', 'celular_smartphone']
    total_tecnologia = sum(row[tecnologia] for tecnologia in tecnologias)
    if total_tecnologia < 3:
        return 'Baja'
    elif 3 <= total_tecnologia <= 7:
        return 'Media'
    else:
        return 'Alta'

data_cleaned['disponibilidad_tecnologia'] = data_cleaned.apply(clasificar_tecnologia, axis=1)

# 3. Disponibilidad de internet (Con internet, Sin internet)
data_cleaned['internet_disponibilidad'] = data_cleaned['internet_fijo'].apply(lambda x: 'Con Internet' if x >= 1 else 'Sin Internet')

# 4. Clasificación por equidad de género (Equilibrada, Hombres predominan, Mujeres predominan)
def clasificar_equidad(hombres, mujeres):
    if hombres == mujeres:
        return 'Equilibrada'
    elif hombres > mujeres:
        return 'Hombres predominan'
    else:
        return 'Mujeres predominan'

data_cleaned['equidad_genero'] = data_cleaned.apply(lambda row: clasificar_equidad(row['hombres_vivienda'], row['mujeres_vivienda']), axis=1)

# Ruta del archivo .shp
archivo_shp = os.path.join('..', 'data', 'raw', 'MAPA', '2023_1_00_ENT.shp')

# Cargar el archivo .shp en un GeoDataFrame
gdf = gpd.read_file(archivo_shp)

diccionario_entidades = {
    "Aguascalientes": 1,
    "Baja California": 2,
    "Baja California Sur": 3,
    "Campeche": 4,
    "Coahuila": 5,
    "Colima": 6,
    "Chiapas": 7,
    "Chihuahua": 8,
    "Ciudad de México": 9,
    "Durango": 10,
    "Guanajuato": 11,
    "Guerrero": 12,
    "Hidalgo": 13,
    "Jalisco": 14,
    "México": 15,
    "Michoacán": 16,
    "Morelos": 17,
    "Nayarit": 18,
    "Nuevo León": 19,
    "Oaxaca": 20,
    "Puebla": 21,
    "Querétaro": 22,
    "Quintana Roo": 23,
    "San Luis Potosí": 24,
    "Sinaloa": 25,
    "Sonora": 26,
    "Tabasco": 27,
    "Tamaulipas": 28,
    "Tlaxcala": 29,
    "Veracruz": 30,
    "Yucatán": 31,
    "Zacatecas": 32
}

# Crear una nueva columna "nombre_entidad" basada en el diccionario
data_cleaned['nombre_entidad'] = data_cleaned['entidad'].map({v: k for k, v in diccionario_entidades.items()})

data_cleaned_file = os.path.join('..', 'data', 'interim', 'vivienda', 'dataset_vivienda.csv')
data_cleaned.to_csv(data_cleaned_file, index=False)

