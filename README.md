# Atom_hacks
Files for app in Sovcombank Team Challenge 2022

# How to Run
## 1. Fork / Clone repo
- fork to your personal repo 
- clone to you local machine

## 2. Use a virtual environment

Сreate and activate virtual environment
```bash
python3 -m venv venv-evraz
echo "export PYTHONPATH=$PWD" >> venv-evraz/bin/activate
source venv-evraz/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```
Run app file
```bash
python AppBank.py
```

# ML-models

Notebook for train final model `FinalSubmission.ipynb` in 'notebook' folder.
The original data is in 'data' folder.
The preprocessed data for train ML-model is in 'data/preprocessed' folder.

# Description task

Разработка приложения для проведения операций на финансовом рынке
Необходимо спроектировать и реализовать приложение для проведения операций на торговых площадках, в частности, на валютном рынке Ожидаемый результат — работающее web/mobile-решение, в рамках которого, реализован обозначенный функционал


# The directory structure
```
├── README.md          <- The top-level README for developers using this project.
│
├── data
│   ├── preprocessed   <- The final, canonical data sets for modeling.
│   
│
├── LPdir              <- Users logins and passwords
│   
│
├── MassData            <- Users phone blacklist and data for new users
│   
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is task name SHKPA-XX (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `SHKPA-67-mms-test-LSTM-model-on-all-electrolyses`.
│
├── PSQL_api           <- Api for database PostgreSQL
│   
│
├── static             <- JS files for app front-end
│   
│
├── SYSTEMmark         <- System mark
│   
├── presentation       <- presentation of our solution
│
│
├── APPBank.py         <- .py file for launch server in Flask
│
├── AppLogs.txt        <- .txt file for application logs
│
├── config.py          <- configuration file (for configure ports)
│
├── logs.log           <- log file
│
├── predictAPI.py      <- .py file for prediction price of currency with 
│
├── .gitignore         <- Avoids uploading data, credentials, outputs, system files etc
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
|
└── src                <- Source code for use in this project.
```

