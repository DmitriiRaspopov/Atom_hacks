from PSQL_api.connect import create_connection
from PSQL_api.queries import execute_query, execute_read_query
from datetime import datetime as dt


def add_account(user_id, connect=False, curr_id='1', description=''):
    """
    Добавление пустого счета. По умолчанию рублевый счет.
    Так же 0 счет, который указывает на пополнение или вывод средств
    :param user_id: user id
    :param connect: объект соединения с БД если создается счет при создании аккаунта
    :param curr_id: id валюты счета
    :param description: дополнительное поле
    :return: успешно или нет

    (1, 'RUB', 'Российский рубль')
    (2, 'USD', 'Доллар США')
    (3, 'CNY', 'Китайский юань')
    (4, 'EUR', 'Евро')
    (5, 'GBP', 'Британский фунт стерлингов')
    (6, 'JPY', 'Японская йена')
    """

    if not connect:
        connect = create_connection()
    connect.autocommit = True
    cursor = connect.cursor()
    if curr_id == 1:
        for crid in [0, 1]:
            query = (f"INSERT INTO accounts (user_id, curr_id, val, description) VALUES %s")
            accnt = [(user_id, crid, 0, description)]
            try:
                cursor.execute(query, accnt)
            except:
                connect.close()
                return False
        connect.close()
    else:
        query = (f"INSERT INTO accounts (user_id, curr_id, val, description) VALUES %s")
        accnt = [(user_id, curr_id, 0, description)]
        try:
            cursor.execute(query, accnt)
            connect.close()
            return True
        except:
            connect.close()
            return False

def get_accounts(user_id):
    """
    Получение всех счетов пользователя с балансом
    :param user_id: user_id
    :return: список счетов с балансом
    """

    accs = []

    connect = create_connection()

    query = (f"SELECT * FROM accounts WHERE user_id = {user_id}")
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        accs = cursor.fetchall()
        connect.close()
        return accs
    except:
        connect.close()
        return accs

def add_money(user_id, value, currh_id='26883', accfr_id='0', curr_id='1'):
    """
    Пополнение рублевого счета. По умолчанию один счет каждой валюты на пользователя
    Так же записать в историю транзакций пополнение счета
    :param user_id: user_id
    :param value: сумма пополнения
    :param currh_id: курс пополнения
    :param accfr_id: источник пополнения
    :param curr_id: валюта счета пополнения
    :return: успешно или нет
    """

    connection = create_connection()
    date = dt.now()
    try:
        print('Проверяю id счет и сумму')
        res_to = execute_read_query(connection, f'SELECT * FROM accounts WHERE user_id = {user_id} AND curr_id = {curr_id}')
        res_from = execute_read_query(connection, f'SELECT * FROM accounts WHERE user_id = {user_id} AND curr_id = {curr_id}')
        connection.close()
    except:
        connection.close()
        return False

    if len(res_to) > 0 and len(res_from) > 0:
        summa = res_to[0][3] + value
        accto_id = res_to[0][0]
        accfr_id = res_from[0][0]
        print(summa, accto_id)
    else:
        return False
    connection = create_connection()
    try:
        print('Пробую внести средства')
        execute_query(connection, f"UPDATE accounts SET val={summa} WHERE id = {accto_id}")
        connection.close()
    except:
        connection.close()
        return False

    connection = create_connection()
    query = (f"INSERT INTO trans (accfr_id, accto_id, user_id, currh_id, date, valfr, valto, description) VALUES %s")
    accnt = [(accfr_id, accto_id, user_id, currh_id, date, value, value, '')]
    cursor = connection.cursor()
    #try:
    print('Добавляю запись в историю операций')
    cursor.execute(query, accnt)
    connection.close()
    return True
    #except:
     #   connection.close()
      #  return False


def out_money(user_id, accfr_id, value, accto_id='0', currh_id='26883', curr_id='1'):
    """
    Вывод средств со счета
    :param user_id: user_id
    :param accfr_id: Источник вывода (должен быть рублевый счет)
    :param value: сумма вывода
    :param accto_id: куда выводятся средства, по умолчанию из системы
    :param currh_id: курс вывода, по умолчанию 1, т.к. рубли без конвертации
    :param curr_id: валюта по умолчанию выводим только с рублевого счета
    :return: успешно или нет
    """

    connection = create_connection()
    date = dt.now()
    try:
        res = execute_read_query(connection, f'SELECT * FROM accounts WHERE user_id = {user_id} AND curr_id = {curr_id}')
        res_to = execute_read_query(connection, f'SELECT * FROM accounts WHERE user_id = {user_id} AND curr_id = {curr_id}')
        connection.close()
    except:
        connection.close()
        return False
    if len(res) > 0 and len(res_to) > 0:
        accfr_id = res[0][0]
        accto_id = res_to[0][0]
        if res[0][3] >= value:
            summa = res[0][3] - value
        else:
            value = res[0][3]
            summa = 0
    else:
        return False
    connection = create_connection()
    try:
        execute_query(connection, f"UPDATE accounts SET val={summa} WHERE id = {accto_id}")
        connection.close()
    except:
        connection.close()
        return False

    connection = create_connection()
    query = (f"INSERT INTO trans (accfr_id, accto_id, user_id, currh_id, date, valfr, valto, description) VALUES %s")
    accnt = [(accfr_id, accto_id, user_id, currh_id, date, value, value, 'Вывод средств')]
    cursor = connection.cursor()
    try:
        cursor.execute(query, accnt)
        connection.close()
        return True
    except:
        connection.close()
        return False

def buy_curr(user_id, value_from, value_to, accfr_id='0', accto_id='0', currh_id='1'):
    """
    Покупка между счетами по курсу. Сами суммы и курс просчитываются на стороне фронта,
    здесь только запись изменений в БД
    :param user_id: user id
    :param value_from: сумма со счета списания в валюте счета
    :param value_to: сумма счета пополнения в валюте счета
    :param accfr_id: id счета списания
    :param accto_id: id счета пополнения
    :param currh_id: id курса валюты по отношению к рублю
    :return: успешно или нет
    """

    connection = create_connection()
    date = dt.now()
    try:
        res_fr = execute_read_query(connection, f'SELECT val FROM accounts WHERE id = {accfr_id}')
        res_to = execute_read_query(connection, f'SELECT val FROM accounts WHERE id = {accto_id}')
        connection.close()
    except:
        connection.close()
        return False
    if len(res_fr) > 0 and len(res_to) > 0:
        summa_fr = res_fr[0][0] - value_from
        summa_to = res_to[0][0] + value_to
    else:
        return False
    connection = create_connection()

    try:
        execute_query(connection, f"UPDATE accounts SET val={summa_fr} WHERE id = {accfr_id}")
        execute_query(connection, f"UPDATE accounts SET val={summa_to} WHERE id = {accto_id}")
        connection.close()
    except:
        connection.close()
        return False

    connection = create_connection()
    query = (f"INSERT INTO trans (accfr_id, accto_id, user_id, currh_id, date, valfr, valto, description) VALUES %s")
    accnt = [(accfr_id, accto_id, user_id, currh_id, date, value_from, value_to, '')]
    cursor = connection.cursor()
    try:
        cursor.execute(query, accnt)
        connection.close()
        return True
    except:
        connection.close()
        return False