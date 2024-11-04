## VARIABLES GLOBALES
PROJECT_NAME = ingCaracteristicasProyecto_
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python3
PYTHON_INTERPRETER_WINDOWS = python 
VENV_DIR = venv
NOMBRE_ENTORNO-VIRTUAL = venv
SISTEMA_OPERATIVO := $(shell uname)
ARCHIVO_DEPENDENCIAS = requirements.txt

## VARIABLES GLOBALES PARA FORMATO DE 'echo'
COLOR_BLUE="\033[1;34m"
COLOR_RESET="\033[0m"

## Linux / Darwin (macOS) / Windows_NT

## script de shell para [Linux / Darwin (macOS)]
SCRIPT_ENTORNO-VIRTUAL_UNIX = ./helpers/setup_env.sh

## scripts .bat para [Windows_NT]
SCRIPT_ENTORNO-VIRTUAL_WINDOWS = .\helpers\setup_env.bat

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
.PHONY: venv 
venv: 
	@if [ "$(SISTEMA_OPERATIVO)" = "Darwin" ] || [ "$(SISTEMA_OPERATIVO)" = "Linux" ]; then \
        echo "   " ; \
        echo ${COLOR_BLUE} "Creando entorno virtual..." ${COLOR_RESET} ; \
        bash $(SCRIPT_ENTORNO-VIRTUAL_UNIX) $(PYTHON_INTERPRETER) $(ARCHIVO_DEPENDENCIAS) $(NOMBRE_ENTORNO-VIRTUAL) ; \
        echo "   " ; \
        echo ${COLOR_BLUE} "Entorno virtual creado." ${COLOR_RESET} ; \
        echo "   " ; \
        echo ${COLOR_BLUE} "Ejecute: source venv/bin/activate. " ${COLOR_RESET} ; \
        echo "   " ; \
    elif [ "$(SISTEMA_OPERATIVO)" = "Windows_NT" ]; then \
        echo "   " ; \
        echo $(COLOR_BLUE) " Creando entorno virtual... " $(COLOR_RESET) ; \
        echo "   " ; \
        ./$(SCRIPT_ENTORNO-VIRTUAL_WINDOWS) ; \
        echo "   " ; \
        echo $(COLOR_BLUE) " Entorno virtual creado. " $(COLOR_RESET) ; \
        echo "   " ; \
    else \
        echo " Sistema operativo no soportado "; \
        exit 1; \
    fi

## Descarga de datos
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

## Reporte de datos
report: venv
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