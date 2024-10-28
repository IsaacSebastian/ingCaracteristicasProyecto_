from ydata_profiling import ProfileReport
#import sweetviz as sv
import pandas as pd
import os

#Para datos de salud mental
ruta_input = [os.path.join('data', 'interim', 'Adolescentes.csv'),
              os.path.join('data', 'interim', 'Adultos.csv'),
              os.path.join('data', 'processed', 'Ensanut-data-p.csv'),
              os.path.join('data', 'interim', '1950.csv'),
              os.path.join('data', 'interim', '1960.csv'),
              os.path.join('data', 'interim', '1970.csv'),
              os.path.join('data', 'interim', '1980.csv'),
              os.path.join('data', 'interim', '1990.csv'),
              os.path.join('data', 'interim', '1995.csv'),
              os.path.join('data', 'interim', '2000.csv'),
              os.path.join('data', 'interim', '2005.csv'),
              os.path.join('data', 'interim', '2010.csv'),
              os.path.join('data', 'interim', '2020.csv')]

ruta_output_y = [os.path.join('docs', 'docs', 'interim-salud-mental-adol-ydata-report.html'),
                 os.path.join('docs', 'docs', 'interim-salud-mental-adul-ydata-report.html'),
                 os.path.join('docs', 'docs', 'interim-salud-mental-adol-adul-ydata-report.html'),
                 os.path.join('docs', 'docs', '1950-ydata-report.html'),
                 os.path.join('docs', 'docs', '1960-ydata-report.html'),
                 os.path.join('docs', 'docs', '1970-ydata-report.html'),
                 os.path.join('docs', 'docs', '1980-ydata-report.html'),
                 os.path.join('docs', 'docs', '1990-ydata-report.html'),
                 os.path.join('docs', 'docs', '1995-ydata-report.html'),
                 os.path.join('docs', 'docs', '2000-ydata-report.html'),
                 os.path.join('docs', 'docs', '2005-ydata-report.html'),
                 os.path.join('docs', 'docs', '2010-ydata-report.html'),
                 os.path.join('docs', 'docs', '2020-ydata-report.html')]

ruta_output_sv = [os.path.join('docs', 'docs','interim-ensa-adol-sweetviz-report.html'),
                  os.path.join('docs', 'docs','interim-ensa-adul-sweetviz-report.html'),
                  os.path.join('docs', 'docs','interim-ensa-adol-adul-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1950-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1960-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1970-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1980-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1990-sweetviz-report.html'),
                  os.path.join('docs', 'docs','1995-sweetviz-report.html'),
                  os.path.join('docs', 'docs','2000-sweetviz-report.html'),
                  os.path.join('docs', 'docs','2005-sweetviz-report.html'),
                  os.path.join('docs', 'docs','2010-sweetviz-report.html'),
                  os.path.join('docs', 'docs','2020-sweetviz-report.html')]

title = ["ENSANUT ADOLESCENTES YData Profiling Report",
         "ENSANUT ADULTOS YData Profiling Report",
         "ENSANUT ADOLESCENTES-ADULTOS YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1950 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1960 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1970 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1980 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1990 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 1995 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 2000 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 2005 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 2010 YData Profiling Report",
         "CENSO DE POBLACION Y VIVIENDA 2020 YData Profiling Report"]
#Ydata

for i in range(13):
    df = pd.read_csv(ruta_input[i], low_memory=False) 
    profile_ensa_ydata = ProfileReport(df, title=title[i], explorative=True, minimal = True)
    profile_ensa_ydata.to_file(ruta_output_y[i])
    print(f"YData report para ENSANUT guardado en {ruta_output_y[i]}")
    #profile_enco_sweetviz = sv.analyze(df)
    #profile_enco_sweetviz.show_html(ruta_output_sv[i])
    #print(f"Sweetviz report para ENSANUT guardado en {ruta_output_sv[i]}")
