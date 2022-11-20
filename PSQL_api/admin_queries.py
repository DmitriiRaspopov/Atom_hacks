from PSQL_api.connect import create_connection
from PSQL_api.queries import execute_query, execute_read_query
from PSQL_api.acc_queries import add_account

def add_user(logname, fname, lname, mname='', phone='', adress='', approved=True, blocked=False, description=''):
    """
    Добавление нового пользователя в БД, заодно создать ему счет в рублях
    :param logname: Логин пользователя
    :param fname: Имя
    :param mname: Отчество
    :param lname: Фамилия
    :param phone: номер телефона
    :param adress: адрес
    :param approved: одобрен к регистрации
    :param blocked: заблокирован
    :param description: дополнительное описание
    :return: успешно или нет
    """

    connect = create_connection()
    query = (f"INSERT INTO users (login, fname, mname, lname, phone, adress, approved, blocked, description) VALUES %s RETURNING id")
    user = [(logname, fname, mname, lname, phone, adress, str(approved), str(blocked), description)]
    connect.autocommit = True
    cursor = connect.cursor()
    try:
        cursor.execute(query, user)
        rid = cursor.fetchall();
        add_account(rid[0][0], connect)
        # connect.close() закрывается при создании счета
        return True;
    except:
        connect.close()
        return False

def block_user(user_id, blocked=False):
    """
    Блокировка пользователя
    :param user_id: user_id
    :return: успешно или нет
    """

    connect = create_connection()
    if blocked:
        blocked = 'TRUE'
    else:
        blocked = 'FALSE'
    #query = (f"UPDATE users SET blocked = {blocked} WHERE id = {user_id}");
    query = (f"UPDATE users SET blocked = {blocked} WHERE login = '{user_id}'");
    connect.autocommit = True
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.close()
        return True;
    except:
        connect.close()
        return False

def get_userinfo(login):
    """
    Получение данных о пользователе
    :param login: login пользователя уникальный
    :return: запись о пользователе
    """

    connect = create_connection()

    query = (f"SELECT * FROM users WHERE login = '{login}'")
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        userinfo = cursor.fetchall()
        connect.close()
        return userinfo
    except:
        connect.close()
        return False
