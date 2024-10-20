#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = ingCaracteristicasProyecto_
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python


DOWNLOAD_SCRIPT_ED=scripts/ed-download-data.py  
PROCESS_SCRIPT_ED=scripts/ed-proc-data.py


#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	



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
.PHONY: create_environment
create_environment:
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	



.PHONY: venv
venv:
	\nworkon $(PROJECT_NAME)
#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

## Download Data
download:venv
	$(PYTHON_EXEC) $(DOWNLOAD_SCRIPT_ED)

## Process Data
process:venv
	$(PYTHON_EXEC) $(PROCESS_SCRIPT_ED)
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
