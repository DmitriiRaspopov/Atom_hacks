#!/usr/bin/python3
# -*- coding: utf-8 -*


import psycopg2
from psycopg2 import OperationalError
import pandas as pd
from datetime import datetime as dt

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def read_data(filename):
    data = pd.read_excel(filename)
    data["data"] = pd.to_datetime(data['data'], dayfirst=True)
#    data.set_index("data", inplace = True)
    data.sort_values("data", inplace = True)
    data.drop(['nominal', 'cdx'], axis=1, inplace=True)
    return data

dbname='scb_db'
user='user'
password='userpass'
host='localhost'
port='5432'

connection = create_connection(dbname, user, password, host, port)
connection.autocommit = True
# первая запись для пополнения/вывода средств с
now = dt.now()
curr_zero = [(1, now, 1)]
insert_query = (f"INSERT INTO currhist (curr_id, date, value) VALUES %s")
cursor = connection.cursor()
cursor.execute(insert_query, curr_zero)

for i in [(2, 'USD', 'USD.xlsx'),
          (3, 'CNY', 'CNY.xlsx'),
          (4, 'EUR', 'EU.xlsx'),
          (5, 'GBP', 'GBP.xlsx'),
          (6, 'JPY', 'JPY.xlsx')]:
    currhist = [];
    currency = read_data(i[2])
    for i in range(len(currency)):
        date, curr = currency.loc[i]
        currhist.append((6, date, curr))

    currhist_records = ", ".join(["%s"] * len(currhist))

    insert_query = (f"INSERT INTO currhist (curr_id, date, value) VALUES {currhist_records}")

    cursor = connection.cursor()
    cursor.execute(insert_query, currhist)

print('all done!')