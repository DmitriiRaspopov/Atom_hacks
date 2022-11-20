import psycopg2
from psycopg2 import OperationalError

def execute_query(connection, query):
    """
    Создание запроса без чтения результата. Можно создавать запись в таблицу
    :param connection:
    :param query:
    :return:
    """
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    """
    Запрос с получением результата
    :param connection:
    :param query:
    :return:
    """
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return result
