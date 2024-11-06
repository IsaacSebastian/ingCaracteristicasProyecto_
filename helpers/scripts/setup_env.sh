#!/bin/bash

# VARIABLES GLOBALES
PYTHON_INTERPRETER="$1"
ARCHIVO_DEPENDENCIAS="$2"
NOMBRE_ENTORNO_VIRTUAL="$3"

# Variables de para los colores de texto impreso con echo
COLOR_YELLOW_MUSTARD="\033[1;33m"
COLOR_RESET="\033[0m"

# Verificar si Python está instalado
if command -v python3 &>/dev/null; then
    echo "Python está instalado."
else
    echo -e "${COLOR_YELLOW_MUSTARD} Python no está instalado. Instalando python...  ${COLOR_RESET}"
    echo "   "
    # Instalar Python 3.10
    sudo apt install -y python3.10
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Python se ha instalado correctamente. ${COLOR_RESET}"
    echo "   "
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null
then
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Pip no está instalado. Instalando pip...${COLOR_RESET}"
    echo "   "
    sudo apt install -y python3-pip
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD}Se ha instalado pip correctamente.${COLOR_RESET}"
    echo "   "
else
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Pip se encuentra instalado. ${COLOR_RESET}"
    echo "   "
fi

# Crear un entorno virtual
echo "   "
echo -e "${COLOR_YELLOW_MUSTARD}Creando un entorno virtual llamado '$3'...${COLOR_RESET}"
echo "   "
$1 -m venv "$3"
echo "   "
echo -e "${COLOR_YELLOW_MUSTARD}Entorno virtual creado entorno virtual llamado 'venv'.${COLOR_RESET}"
echo "   "

# Activar el entorno virtual
echo "   "
#echo "Activando el entorno virtual..."
#echo "   "
#source venv/bin/activate
#echo "   "
#echo "Entorno virtual activado."
echo "   "

# Verificar si requirements.txt existe
if [ -f "$2" ]; then
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Para instalar dependencias dependencias desde requirements.txt ...${COLOR_RESET}"
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Ejecute el comando: pip install -q -r $2 ${COLOR_RESET}"
    # pip install -q -r "$2"
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} Para instalar dependencias dependencias desde requirements.txt ...${COLOR_RESET}"
    echo -e "${COLOR_YELLOW_MUSTARD} Para activar el entorno virtual ejecute el siguiente comando... ${COLOR_RESET}"
    echo -e "${COLOR_YELLOW_MUSTARD} Ejecute: source $3/bin/activate ${COLOR_RESET}"
    echo "   "
    #echo -e "${COLOR_YELLOW_MUSTARD}Las dependencias de requirements.txt han sido instaladas correctamente.${COLOR_RESET}"
    echo "   "
else
    echo "   "
    echo -e "${COLOR_YELLOW_MUSTARD} requirements.txt no encontrado. No se instalarán dependencias.${COLOR_RESET}"
    echo "   "
fi

echo "   "
echo -e "${COLOR_YELLOW_MUSTARD}Solo falta activar el entorno virtual con 'source venv/bin/activate' y las dependencias han sido instaladas.${COLOR_RESET}"
echo "   "