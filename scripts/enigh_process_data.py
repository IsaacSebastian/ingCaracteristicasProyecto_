import os
import pandas as pd

PROCESSED_PATH="data/processed/ENIGH"
RAW_PATH="data/raw/DATOS EDUCACION/ENCUESTA NACIONAL DE INGRESOS Y GASTOS EN LOS HOGARES/Extracted"


# -----------------  Data paths ------------------------ #

population_data=[f"{RAW_PATH}/2016/conjunto_de_datos_poblacion_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2016_ns.csv"
                ,f"{RAW_PATH}/2018/conjunto_de_datos_poblacion_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2018_ns.csv"
                ,f"{RAW_PATH}/2020/conjunto_de_datos_poblacion_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh_2020_ns.csv"
                ,f"{RAW_PATH}/2022/conjunto_de_datos_poblacion_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_poblacion_enigh2022_ns.csv"]


income_personal_data=[f"{RAW_PATH}/2016/conjunto_de_datos_ingresos_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2016_ns.csv"
                ,f"{RAW_PATH}/2018/conjunto_de_datos_ingresos_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2018_ns.csv"
                ,f"{RAW_PATH}/2020/conjunto_de_datos_ingresos_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh_2020_ns.csv"
                ,f"{RAW_PATH}/2022/conjunto_de_datos_ingresos_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_ingresos_enigh2022_ns.csv"]

bills_personal_data=[f"{RAW_PATH}/2016/conjunto_de_datos_gastospersona_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_gastospersona_enigh_2016_ns.csv"
                ,f"{RAW_PATH}/2018/conjunto_de_datos_gastospersona_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_gastospersona_enigh_2018_ns.csv"
                ,f"{RAW_PATH}/2020/conjunto_de_datos_gastospersona_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_gastospersona_enigh_2020_ns.csv"
                ,f"{RAW_PATH}/2022/conjunto_de_datos_gastospersona_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_gastospersona_enigh2022_ns.csv"]

bills_house_data=[f"{RAW_PATH}/2016/conjunto_de_datos_gastoshogar_enigh_2016_ns/conjunto_de_datos/conjunto_de_datos_gastoshogar_enigh_2016_ns.csv"
                ,f"{RAW_PATH}/2018/conjunto_de_datos_gastoshogar_enigh_2018_ns/conjunto_de_datos/conjunto_de_datos_gastoshogar_enigh_2018_ns.csv"
                ,f"{RAW_PATH}/2020/conjunto_de_datos_gastoshogar_enigh_2020_ns/conjunto_de_datos/conjunto_de_datos_gastoshogar_enigh_2020_ns.csv"
                ,f"{RAW_PATH}/2022/conjunto_de_datos_gastoshogar_enigh2022_ns/conjunto_de_datos/conjunto_de_datos_gastoshogar_enigh2022_ns.csv"]



# -----------------  Transformations ------------------------ #

#  Personal Bills 
year=2016
dataframe_list=[]
for file_path in bills_personal_data:
    columns_interest=['folioviv', 'foliohog', 'numren', # Primary key 
                   'clave', 'mes_dia', 'forma_pag1', 'forma_pag2', 'forma_pag3', 'inscrip',
                   'colegia', 'material', 'cantidad', 'gasto', 'costo', 'gasto_tri']

    df=pd.read_csv(file_path)
    df=df[columns_interest]
    
    fill_columns=['cantidad','gasto','costo','gasto_tri']

    for column in fill_columns:
        if df[column].dtype=='object':
            df[column]=df[column].str.replace(' ','0')
    

    formats={
        'clave':'string',
        'cantidad':'float',
        'gasto':'float',
        'costo':'float',
        'gasto_tri':'float',
        'year':'int'
    }

    df['entidad']=df['folioviv']//10**8
    df['year']=year
    
    df=df.astype(formats)
    df=df.rename(columns={'clave':'clave_gasto'})
    dataframe_list.append(df)
    year+=2
    

bills_personal=pd.concat(dataframe_list)

#  House Bills 
year=2016
dataframe_list=[]
for file_path in bills_house_data:
    columns_interest=['folioviv', 'foliohog', # Primary key 
                   'clave', 'gasto', 'costo', 'gasto_tri']

    df=pd.read_csv(file_path)
    df=df[columns_interest]
    
    fill_columns=['gasto','costo','gasto_tri']

    for column in fill_columns:
        if df[column].dtype=='object':
            df[column]=df[column].str.replace(' ','0')
    

    formats={
        'clave':'string',
        'gasto':'float',
        'costo':'float',
        'gasto_tri':'float',
        'year':'int'
    }

    df['entidad']=df['folioviv']//10**8
    df['year']=year
    
    df=df.astype(formats)
    df=df.rename(columns={'clave':'clave_gasto_h','gasto_tri':'gasto_tri_h','gasto':'gasto_h'})
    dataframe_list.append(df)
    year+=2
    

bills_house=pd.concat(dataframe_list)

# ----- Income ---------
year=2016
dataframe_list=[]
for file_path in income_personal_data:
    columns_interest=['folioviv', 'foliohog', 'numren' # Primary key 
                     ,'clave','ing_tri']

    df=pd.read_csv(file_path)
    df=df[columns_interest]
    
    

    formats={
        'clave':'string',
        'ing_tri':'float',
        'year':'int'
    }

    df['entidad']=df['folioviv']//10**8
    df['year']=year
    
    df=df.astype(formats)
    df=df.rename(columns={'clave':'clave_ingreso'})
    dataframe_list.append(df)
    year+=2
    

income=pd.concat(dataframe_list)


# ----- Population --------  
dataframe_list=[]
year=2016
for file_path in population_data:
    
    columns_interest=[
        'folioviv', 'foliohog', 'numren', # Primary key
        'parentesco', 'sexo', 'edad',
        'alfabetism','asis_esc', 'nivel', 'grado', 'tipoesc', 'tiene_b',
        'forma_b', 'tiene_c', 'forma_c', 'nivelaprob', 'gradoaprob',
        'antec_esc', 'residencia', 'diabetes', 'pres_alta', 'peso','num_trabaj'
    ]

    df=pd.read_csv(file_path)
    df=df[columns_interest]

    fill_column=['nivel','grado','alfabetism','tipoesc','asis_esc','antec_esc','num_trabaj','nivelaprob','gradoaprob']
    for column in fill_column:
        if df[column].dtype=='object':
            df[column]=df[column].str.replace(' ','0')     
        else:
            df[column]=df[column].fillna(0)

    formats={
        'alfabetism':'int64',
        'asis_esc':'int64',
        'nivel':'int64',
        'grado':'int64',
        'tipoesc':'int64',
        'nivelaprob':'int64',
        'gradoaprob':'int64'
    }
    df['entidad']=df['folioviv']//10**8
    df['year']=year

    bins = [1901,1924,1945, 1964, 1980, 1996, 2012, 2024 ]  # Generation birth ranges
    labels = ['Greatest','Silent','Baby Boomer', 'X', 'Milenial', 'Z','Alpha']  # Generation labels

    df['año_nacimiento']=df['year']-df['edad']
    df['generacion'] = pd.cut(df['año_nacimiento'], bins=bins, labels=labels, right=True)
    df.drop(columns='año_nacimiento', inplace=True)

    df=df.astype(formats)
    dataframe_list.append(df)
    year+=2

population=pd.concat(dataframe_list)

entity_catalogue=f"{RAW_PATH}/2022/conjunto_de_datos_poblacion_enigh2022_ns/catalogos/entidad.csv"
entity=pd.read_csv(entity_catalogue,encoding='Windows-1252')

population=pd.merge(population,entity, on='entidad',how='inner')
population=population.rename(columns={'descripcion':'nombre_entidad'})


# --- Save data -----

os.makedirs(PROCESSED_PATH,exist_ok=True)

bills_personal.to_csv(f"{PROCESSED_PATH}/bills_personal.csv")

bills_house.to_csv(f"{PROCESSED_PATH}/bills_house.csv")

income.to_csv(f"{PROCESSED_PATH}/income.csv")

population.to_csv(f"{PROCESSED_PATH}/population.csv")

