#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = ingCaracteristicasProyecto_
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python3
VENV_DIR=venv

DOWNLOAD_SCRIPT_ED=scripts/ed-download-data.py  
DOWNLOAD_SCRIPT_SM=scripts/sm-download-data.py  
PROCESS_SCRIPT_ED=scripts/ed-proc-data.py  
PROCESS_SCRIPT_SM=scripts/sm-inter-proc-data.py
REPORT_SCRIPT_ED_SM=scripts/Ydata-SweetViz-datasets.py


# Detect OS
ifeq ($(OS),Windows_NT)
    # Windows 
    VENV_ACTIVATE=$(VENV_DIR)\Scripts\activate.bat
    PYTHON_EXEC=$(VENV_DIR)\Scripts\python
    PIP_EXEC=$(VENV_DIR)\Scripts\pip
else
    # macOS/Linux
    VENV_ACTIVATE=$(VENV_DIR)/bin/activate
    PYTHON_EXEC=$(VENV_DIR)/bin/python3
    PIP_EXEC=$(VENV_DIR)/bin/pip3
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PIP_EXEC) install --upgrade pip setuptools wheel numpy
	$(PIP_EXEC) install -r requirements.txt -v
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 ingcaracteristicasproyecto
	isort --check --diff --profile black ingcaracteristicasproyecto
	black --check --config pyproject.toml ingcaracteristicasproyecto

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml ingcaracteristicasproyecto




## Set up python interpreter environment
.PHONY: environment
environment:
	python3 -m venv $(VENV_DIR)
	

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Download Data
download:
	$(PYTHON_EXEC) $(DOWNLOAD_SCRIPT_ED)
	$(PYTHON_EXEC) $(DOWNLOAD_SCRIPT_SM)

## Process Data
process:
	$(PYTHON_EXEC) $(PROCESS_SCRIPT_ED)
	$(PYTHON_EXEC) $(PROCESS_SCRIPT_SM)

report:
	$(PYTHON_EXEC) $(REPORT_SCRIPT_ED_SM)
## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) ingcaracteristicasproyecto/dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
