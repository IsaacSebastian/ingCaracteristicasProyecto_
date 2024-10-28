![MCD](https://mcd.unison.mx/wp-content/themes/awaken/img/logo_mcd.png)
# Educación y Salud Mental en México 

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

Proyecto de ingeniería de características 2024-2
-------------------------------------------------------------------------
Objective:

This project was created to complete assignments within the master's program in Data Science. It aims to analyze potential relationships between mental health and education among Mexican youth. Our goal is to answer the following questions:

Is there a relationship between academic performance and students' mental health?

In which part of the country is school dropout or mental health issues more prevalent, and could they be related?

Does school belonging correlate with mental health among Mexican youth?

We hope to answer these questions and communicate our findings to the general public and education leaders.

Data Sources:

For education-related data in Mexico, we will use INEGI survey results and a 2023 SEP report on educational indicators. We will also reference the General Census of Population and Housing for georeferenced and temporal data on Mexican students, along with the National Survey on Access and Continuity in Education (ENAPE) 2021 to generate statistics on educational access and continuity among individuals aged 0-29.

For mental health data, our main source will be the National Health and Nutrition Survey (ENSANUT), which began in 2000. Initially planned as a six-year survey, it was also conducted in 2016 and annually since 2020. This survey has two main sections—health and nutrition—and each is divided into adolescent and adult segments. In this project, all available data catalogs and questionnaires will be collected and analyzed to identify information related to mental health for our target age groups.

We will then aim to integrate the education and mental health data for a coherent statistical analysis.
## Project Organization

```
├── LICENSE            <- Open-source license if one is chosen
├── Makefile           <- Makefile with convenience commands like `make data` or `make train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- Data from third party sources.
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump.
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for 
│                         ingcaracteristicasproyecto and configuration for tools like black
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.cfg          <- Configuration file for flake8
│
└── ingcaracteristicasproyecto   <- Source code for use in this project.
    │
    ├── __init__.py             <- Makes ingcaracteristicasproyecto a Python module
    │
    ├── config.py               <- Store useful variables and configuration
    │
    ├── dataset.py              <- Scripts to download or generate data
    │
    ├── features.py             <- Code to create features for modeling
    │
    ├── modeling                
    │   ├── __init__.py 
    │   ├── predict.py          <- Code to run model inference with trained models          
    │   └── train.py            <- Code to train models
    │
    └── plots.py                <- Code to create visualizations
```

--------

## Ejecutando proyecto

1. First, clone the repository by running:
    ```bash
    git clone https://github.com/IsaacSebastian/ingCaracteristicasProyecto_
    ```

2. Next, navigate to the repository:
    ```bash
    cd ingCaracteristicasProyecto_
    ```

3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:
    ```bash
    venv\Scripts\activate
    ```

5. Install dependencies listed in 'requirements.txt':
    ```bash
    make requirements 
    ```

6. Download both data sets:
    ```bash
    make download 
    ```

7. Process both data sets:
    ```bash
    make process
    ```


# Licencia
This project is under the MIT license.
