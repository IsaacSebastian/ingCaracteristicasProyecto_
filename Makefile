## VARIABLES GLOBALES
PROJECT_NAME = ingCaracteristicasProyecto_
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python3
PYTHON_INTERPRETER_WINDOWS = python
VENV_DIR = venv
DVC = dvc
DATA_DIR = data/raw
INTERIM_DIR=data/interim
NOMBRE_ENTORNO-VIRTUAL = venv
SISTEMA_OPERATIVO := $(shell uname)
ARCHIVO_DEPENDENCIAS = ./requirements.txt
REPOSITORIO_URL = https://github.com/IsaacSebastian/ingCaracteristicasProyecto_.git
GESTOR_PAQUETES = pip
PYTHON_INSTALLER_EXE_URL = https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe
PYTHON_INSTALLER_EXE_NAME = python_installer_v3.11.4.exe

## VARIABLES GLOBALES PARA FORMATO DE 'echo'
COLOR_BLUE="\033[1;34m"
COLOR_RESET="\033[0m"

## Linux / Darwin (macOS) / Windows_NT

## script de shell para [Linux / Darwin (macOS)]
SCRIPT_ENTORNO-VIRTUAL_UNIX = ./helpers/scripts/setup_env.sh

## scripts .bat para [Windows_NT]
SCRIPT_ENTORNO-VIRTUAL_WINDOWS = .\helpers\scripts\setup_env.bat

## Rutas de scripts para [Linux / Darwin (macOS)]
DOWNLOAD_SCRIPT_ED = scripts/ed-download-data.py
PROCESS_SCRIPT_ED = scripts/ed-proc-data.py
DOWNLOAD_SCRIPT_SM = scripts/sm-download-data.py
PROCESS_SCRIPT_SM = scripts/sm-proc-data.py

## Rutas de scripts para [Windows_NT]
DOWNLOAD_SCRIPT_ED_WINDOWS = scripts\ed-download-data.py
PROCESS_SCRIPT_ED_WINDOWS = scripts\ed-proc-data.py
DOWNLOAD_SCRIPT_SM_WINDOWS = scripts\sm-download-data.py
PROCESS_SCRIPT_SM_WINDOWS = scripts\sm-proc-data.py

## Ejecutar reportes Ydata
REPORT_SCRIPT_WINDOWS = scripts\Ydata-datasets.py
REPORT_SCRIPT = scripts/Ydata-datasets.py

## Install: python , pip , create virtual environment , python dependencies 
.PHONY: venv download raw_data

# Create virtual environment
venv: 
	@if [ "$(SISTEMA_OPERATIVO)" = "Darwin" ] || [ "$(SISTEMA_OPERATIVO)" = "Linux" ]; then \
        echo "   " ; \
        echo ${COLOR_BLUE} "Creating virtual environment..." ${COLOR_RESET} ; \
        bash $(SCRIPT_ENTORNO_VIRTUAL_UNIX) $(PYTHON_INTERPRETER) $(ARCHIVO_DEPENDENCIAS) $(NOMBRE_ENTORNO_VIRTUAL) ; \
        echo "   " ; \
        echo ${COLOR_BLUE} "Virtual environment created." ${COLOR_RESET} ; \
        echo "   " ; \
        . venv/bin/activate ; \
        echo ${COLOR_BLUE} "Virtual environment activated." ${COLOR_RESET} ; \
        pip install -q -r requirements.txt ; \
        echo ${COLOR_BLUE} "Dependencies installed!" ${COLOR_RESET} ; \
        echo "   " ; \
    elif [ "$(SISTEMA_OPERATIVO)" = "Windows_NT" ]; then \
        echo "   " ; \
        echo $(COLOR_BLUE) "Creating virtual environment..." $(COLOR_RESET) ; \
        echo "   " ; \
        ./$(SCRIPT_ENTORNO_VIRTUAL_WINDOWS) $(PYTHON_INTERPRETER) $(ARCHIVO_DEPENDENCIAS) $(NOMBRE_ENTORNO_VIRTUAL) ${REPOSITORIO_URL} ${PYTHON_INSTALLER_EXE_URL} ${PYTHON_INSTALLER_EXE_NAME} ; \
        echo "   " ; \
        echo $(COLOR_BLUE) "Virtual environment created." $(COLOR_RESET) ; \
        echo ${COLOR_BLUE} "Execute: ' source venv/bin/activate ' to activate the virtual environment." ${COLOR_RESET} ; \
        echo ${COLOR_BLUE} "Execute: ' pip install -q -r requirements.txt ' to install dependencies." ${COLOR_RESET} ; \
        echo "   " ; \
    else \
        echo "Unsupported operating system"; \
        exit 1; \
    fi

## Descarga de datos


.PHONY: download
download: venv
	@if [ "$(SISTEMA_OPERATIVO)" = "Darwin" ] || [ "$(SISTEMA_OPERATIVO)" = "Linux" ]; then \
        echo $(COLOR_BLUE) "Realizando descarga de datos..." $(COLOR_RESET) ; \
        echo "   " ; \
        $(PYTHON_INTERPRETER) $(DOWNLOAD_SCRIPT_ED) ; \
        $(PYTHON_INTERPRETER) $(DOWNLOAD_SCRIPT_SM) ; \
        echo "   " ; \
        echo $(COLOR_BLUE) "Descarga de datos realizada correctamente."  $(COLOR_RESET); \
        echo "   " ; \
    elif [ "$(SISTEMA_OPERATIVO)" = "Windows_NT" ]; then \
        echo "   " ; \
        echo $(COLOR_BLUE) "Realizando descarga de datos..."  $(COLOR_RESET) ; \
        echo "   " ; \
        $(PYTHON_INTERPRETER_WINDOWS) $(DOWNLOAD_SCRIPT_ED_WINDOWS); \
        $(PYTHON_INTERPRETER_WINDOWS) $(DOWNLOAD_SCRIPT_SM_WINDOWS); \
        echo "   " ; \
        echo $(COLOR_BLUE) "Descarga de datos realizada correctamente." $(COLOR_RESET) ; \
        echo "   " ; \
    else \
        echo "Sistema operativo no soportado"; \
        exit 1; \
    fi

raw_data:download
	$(VENV_DIR)/bin/dvc add $(DATA_DIR)
	@echo "Raw data added to DVC"
    
## Procesamiento de datos
.PHONY: process
process: venv download
	@if [ "$(SISTEMA_OPERATIVO)" = "Darwin" ] || [ "$(SISTEMA_OPERATIVO)" = "Linux" ]; then \
        echo "   " ; \
        echo $(COLOR_BLUE) "Realizando procesamiento de datos..." $(COLOR_RESET); \
        echo "   " ; \
        $(PYTHON_INTERPRETER) $(PROCESS_SCRIPT_ED) ; \
        $(PYTHON_INTERPRETER) $(PROCESS_SCRIPT_SM) ; \
        echo "   " ; \
        echo $(COLOR_BLUE) "Procesamientos de datos realizada correctamente." $(COLOR_RESET) ; \
        echo "   " ; \
    elif [ "$(SISTEMA_OPERATIVO)" = "Windows_NT" ]; then \
        echo "   " ; \
        echo $(COLOR_RESET) "Realizando procesamiento de datos..." $(COLOR_RESET) ; \
        echo "   " ; \
        $(PYTHON_INTERPRETER_WINDOWS) $(PROCESS_SCRIPT_ED_WINDOWS) ; \
        $(PYTHON_INTERPRETER_WINDOWS) $(PROCESS_SCRIPT_SM_WINDOWS) ; \
        echo "   " ; \
        echo $(COLOR_BLUE) "Procesamiento de datos realizada correctamente." $(COLOR_RESET); \
        echo "   " ; \
    else \
        echo "Sistema operativo no soportado"; \
        exit 1; \
    fi

interim_data:process
	$(DVC) add $(INTERIM_DIR)
	@echo "Add interim data to DVC"
    

## Reporte de datos
.PHONY: report-ydata
report-ydata: venv download process
	@if [ "$(SISTEMA_OPERATIVO)" = "Darwin" ] || [ "$(SISTEMA_OPERATIVO)" = "Linux" ]; then \
        echo $(COLOR_BLUE) "Creando reportes Y-data..." $(COLOR_RESET) ; \
        echo "   " ; \
        $(PYTHON_INTERPRETER) $(REPORT_SCRIPT) ; \
        echo "   " ; \
        echo $(COLOR_BLUE) "Reportes creados exitosamente."  $(COLOR_RESET); \
        echo "   " ; \
    elif [ "$(SISTEMA_OPERATIVO)" = "Windows_NT" ]; then \
        echo "   " ; \
        echo $(COLOR_BLUE) "Creando reportes Y-data..."  $(COLOR_RESET) ; \
        echo "   " ; \
        $(PYTHON_INTERPRETER_WINDOWS) $(REPORT_SCRIPT_WINDOWS); \
        echo "   " ; \
        echo $(COLOR_BLUE) "Reportes creados exitosamente." $(COLOR_RESET) ; \
        echo "   " ; \
    else \
        echo "Sistema operativo no soportado"; \
        exit 1; \
    fi