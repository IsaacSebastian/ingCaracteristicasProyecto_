@echo off

REM Recivir parametros
SET PYTHON_INTERPRETER=%1
SET ARCHIVO_DEPENDECIAS=%2
SET NOMBRE_ENTORNO-VIRTUAL=%3
SET REPOSITORIO_URL=%4
SET PYTHON_INSTALLER_EXE_URL=%5
SET PYTHON_INSTALLER_EXE_NAME=%6

REM Variables globales

:: ------------------------------------------
:: Asignacion de colores para los echos

    :: 0 = Negro       8 = Gris
    :: 1 = Azul        9 = Azul claro
    :: 2 = Verde       A = Verde claro
    :: 3 = Aguamarina  B = Aguamarina claro
    :: 4 = Rojo        C = Rojo claro
    :: 5 = Púrpura     D = Púrpura claro
    :: 6 = Amarillo    E = Amarillo claro
    :: 7 = Blanco      F = Blanco brillante
:: ------------------------------------------

REM Imprimir parametros
::echo parametro_1: %1
::echo parametro_2: %2
::echo parametro_3: %3
::echo parametro_4: %4

REM Imprimir parametros
IF "%1"=="" (
    echo No se proporcionó el primer argumento. Proporcione todos los argumentos necesarios.
    exit /b 1
) ELSE (
    echo El primer argumento es: %1
)

IF "%2"=="" (
    echo No se proporcionó el segundo argumento. Proporcione todos los argumentos necesarios.
    exit /b 1
) ELSE (
    echo El segundo argumento es: %2
)

IF "%3"=="" (
    echo No se proporcionó el tercer argumento. Proporcione todos los argumentos necesarios.
    exit /b 1
) ELSE (
    echo El tercer argumento es: %3
)

IF "%4"=="" (
    echo No se proporcionó el cuarto argumento. Proporcione todos los argumentos necesarios.
    exit /b 1
) ELSE (
    echo El cuarto argumento es: %4
)

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
 
    echo Python no esta instalado.
    
    echo "   "
    
    echo "   "
    echo Python y PIP no esta instalados. Procederemos ha la instalacion de Python y PIP.
    echo "   "

    REM Descarga del ejecutable .exe de python.
    echo "   "
    echo "Descargando instalador de python.exe con 'curl'... "
    curl -o ./%PYTHON_INSTALLER_EXE_NAME% %PYTHON_INSTALLER_EXE_URL%
    echo "Descargando instalador de python.exe"
    echo "   "

    REM Realizando instalacion de python.
    echo "   "
    echo "Realizando instalacion de python..."
    %PYTHON_INSTALLER_EXE_NAME%
    echo "Instalacion de python realizada correctamente"
    echo "   "

    REM Se elimina ejecutable .exe , instalador de python.
    echo "   "
    echo "Eliminando archivo .exe ..."
    del %PYTHON_INSTALLER_EXE_NAME%
    echo "Archivo eliminado .exe"
    echo "   "

    REM Para crear entorno virtual.
    echo "   "
    echo "Creando entorno virtual..."
    %PYTHON_INTERPRETER% -m venv %NOMBRE_ENTORNO-VIRTUAL%
    echo "Entorno virtual creado."
    echo "   "
    
    REM Para activar entorno virtual.
    echo "   "
    echo "Para activar entorno virtual..."
    echo " Para activar entorno virtual ejecute: venv\Scripts\activate "
    echo "   "

    REM Se instalan dependecias en el ambiente virtual creado.
    echo "   "
    echo "Instalando dependecinas con reuirements.txt ..."
    REM pip install -r requirements.txt
    echo " Ejecute: pip install -r requirements.txt"
    echo "   "

    echo Repositorio url: %4
    echo "   "

    exit /b 1
    
) 
ELSE (
    
    echo ----------------------------------------------------
    
    REM Mostrando versiones de Python y Pip.
    echo "   "
    echo Python y PIP estan instalados.
    echo Repositorio url: %4
    echo La version de Python: 
    python --version
    echo La version de Pip: 
    pip --version
    echo "   "

    REM Para crear entorno virtual.
    echo "   "
    echo "Creando entorno virtual..."
    %PYTHON_INTERPRETER% -m venv %NOMBRE_ENTORNO-VIRTUAL%
    echo "Entorno virtual creado."
    echo "   "
    
    REM Para activar entorno virtual.
    echo "   "
    echo "Para activar entorno virtual..."
    echo " Para activar entorno virtual ejecute: venv\Scripts\activate "
    echo "   "

    REM Se instalan dependecias en el ambiente virtual creado.
    echo "   "
    echo "Instalando dependecinas con reuirements.txt ..."
    echo " Ejecute: pip install -r requirements.txt"
    echo "   "

    echo Repositorio url: %4
    echo "   "

    REM SET /p valor= Actualizar python: [s/n]: 
    REM pause

    REM IF %valor%=="s" (
    REM    echo Actualizando python ...
    REM ) 
    REM ELSE IF %valor%=="S" (
    REM    echo Actualizando python ...
    REM )
    REM ELSE IF %valor%=="n" (
    REM    echo Has ingresado un valor diferente de ['S', 's' , 'N', 'n' ].
    REM )
    REM ELSE (
    REM    echo Has ingresado un valor diferente de ['S', 's' , 'N', 'n'].
    REM )

    echo ----------------------------------------------------
)

