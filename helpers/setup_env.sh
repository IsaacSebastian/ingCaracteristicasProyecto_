#!/bin/bash

# VARIABLES GLOBALES
PYTHON_INTERPRETER="$1"
ARCHIVO_DEPENDENCIAS="$2"
NOMBRE_ENTORNO_VIRTUAL="$3"

ROJO="\e[31m"
NEGRITA="\e[1m"
RESET="\e[0m"

echo -e "${NEGRITA}${ROJO}Todos los argumentos: $@${RESET}"
echo "   "

# Verificar si pip está instalado
if ! command -v pip &> /dev/null
then
    echo "pip no está instalado. Instalando pip..."
    echo "   "
    sudo apt install -y python3-pip
    echo "   "
    echo "Se ha instalado pip correctamente."
fi

# Crear un entorno virtual
echo "Creando un entorno virtual llamado 'venv'..."
echo "   "
python3 -m venv venv
echo "   "
echo "Entorno virtual creado entorno virtual llamado 'venv'."

# Activar el entorno virtual
echo "Activando el entorno virtual..."
echo "   "
source venv/bin/activate
echo "   "
echo "Entorno virtual activado."

# Verificar si requirements.txt existe
if [ -f "requirements.txt" ]; then
    echo "Instalando dependencias desde requirements.txt ..."
    echo "   "
    echo "   "
    echo "   "
    pip install -r requirements.txt
    echo "   "
    echo "   "
    echo "   "
    echo "Las dependencias de requirements.txt han sido instaladas correctamente."
else
    echo "   "
    echo "requirements.txt no encontrado. No se instalarán dependencias."
    echo "   "
fi

echo "   "
echo "Todo listo. El entorno virtual está activo y las dependencias han sido instaladas."
echo "   "