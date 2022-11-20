# Atom_hacks
Files for app in Sovcombank Team Challenge 2022

# How to Run
## 1. Fork / Clone repo
- fork to your personal repo 
- clone to you local machine

## 2. Use a virtual environment

Сreate and activate virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```bash
pip install -r requirements.txt
```
## 3. Run app file
```bash
python AppBank.py
```

## 4. Database configure

### Launch postgres

```
cd postgres && docker-compose up
```
#### Получение курсов валют:
    API от api.apilayer.com
    
#### База данных:
    В отдельном контейнере развернута PostgreSQL
    Доступ к базе данных осуществляется посредством SQL запросов через обертку для python - psycopg2
    
#### Фукционал обращений к БД:
    * Добавление нового пользователя
    * Блокировка / разблокировка пользователя
    * Получение информации о пользователе
    * Получение информации о счетах пользователя
    * История покупок / продаж валюты по пользователю
    * Добавление нового счета (рублевый добавляется одновременно с пользователем по умолчанию)
    * Пополнение рублевого счета
    * Вывод денег с рублевого счета
    * Покупка валюты по текущему курсу при условии открытого счета для этой валюты за рубли
    * Продажа валюты - перевод денежных средств с валютного счета в рублевый по текущему курсу
    * Запись новых курсов валют
    * Запрос истории курсов валют

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
├── postgres           <- docker-compose file for launch postgres
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
```

