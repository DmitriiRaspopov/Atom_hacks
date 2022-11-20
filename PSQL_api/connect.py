import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name = 'scb_db',
                      db_user = 'user',
                      db_password = 'userpass',
                      db_host = 'localhost',
                      db_port = '5432'):
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
