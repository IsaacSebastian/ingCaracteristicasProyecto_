@echo off

REM Verificar si Python ya está instalado
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Instalando Python...
    REM Aquí puedes agregar el enlace de descarga de Python para Windows
    REM Por ejemplo, usar el instalador de Python
    start /wait "" "https://www.python.org/ftp/python/3.10.12/python-3.10.12-amd64.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
) ELSE (
    echo Python ya está instalado.
)

REM Verificar si pip está instalado
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Instalando pip...
    REM Descargar el script de instalación de pip
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    del get-pip.py
) ELSE (
    echo pip ya está instalado.
)

REM Crear un entorno virtual
echo Creando un entorno virtual...
python -m venv myenv

REM Activar el entorno virtual
echo Activando el entorno virtual...
call myenv\Scripts\activate

REM Instalar los requisitos
echo Instalando los requisitos desde requirements.txt...
pip install -r requirements.txt

echo Proceso completado.
pause
