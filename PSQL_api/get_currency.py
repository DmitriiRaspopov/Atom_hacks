import requests, json
from datetime import datetime as dt
from PSQL_api.connect import create_connection
from PSQL_api.queries import execute_read_query
import pandas as pd
import plotly.express as px
import io
from base64 import b64encode

def get_currency():
    """
    АПИ получения биржевого курса валют и записи его в БД
    :return: возвращает json вида:
    {'success': True,
     'timestamp': datetime.datetime(2022, 11, 19, 21, 34, 2),
     'source': 'RUB',
     'quotes': {'RUBUSD': 60.849458439819884,
                'RUBEUR': 62.95247088448222,
                'RUBGBP': 72.34319612240469,
                'RUBJPY': 0.43357688792384314,
                'RUBCNY': 8.546497218115155}}
    """
    source = 'RUB'
    currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']
    url = f"https://api.apilayer.com/currency_data/live?source={source}&currencies=USD,EUR,GBP,JPY,CNY"
    payload = {}
    headers = {"apikey": "dKVEwmVT5jK8bt82bI84g4GRbjXRd1oZ"}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200:
        res = json.loads(response.text)
        if not res['success']:
            return False
        for pairs in res['quotes']:
            val = 1 / res['quotes'][pairs]
            res['quotes'][pairs] = val

        date = dt.utcfromtimestamp(res['timestamp'])
        res['timestamp'] = date

        currhist = [
            (2, date, res['quotes']['RUBUSD']),
            (3, date, res['quotes']['RUBCNY']),
            (4, date, res['quotes']['RUBEUR']),
            (5, date, res['quotes']['RUBGBP']),
            (6, date, res['quotes']['RUBJPY']),
        ]
        currhist_records = ", ".join(["%s"] * len(currhist))
        insert_query = (f"INSERT INTO currhist (curr_id, date, value) VALUES {currhist_records}")

        connect = create_connection()
        connect.autocommit = True
        cursor = connect.cursor()
        try:
            cursor.execute(insert_query, currhist)
            return res
        except:
            return False

def get_curr_rates(curr=[], period=None):
    """
    Функция генерирует график истории изменения курса валют или нескольких валют.
    На данный момент берутся все имеющиеся данные
    :param curr: список id валют
    :param period: период, за который необходимо взять исторические данные
    :return: график, готовый для отображения на странице html

    Макс, посмотри код из примера, с помощью которого можно отображать полученный результат:
    Я надеюсь ты понимаешь что тут написано и это подходит

    html.Div([
    html.H4('Simple plot export options'),
    html.P("↓↓↓ try downloading the plot as PNG ↓↓↓", style={"text-align": "right", "font-weight": "bold"}),
    dcc.Graph(id="graph", figure=fig),
    html.A(
        html.Button("Download as HTML"),
        id="download",
        href="data:text/html;base64," + encoded, <===== вот здесь параметр encoded  - это от функции отправляется тебе
        download="plotly_graph.html"
    )
])

    """
    buffer = io.StringIO()
    if len(curr) == 0:
        select_curr = "SELECT * FROM currhist INNER JOIN currency ON currhist.curr_id=currency.id WHERE curr_id != 0 ORDER BY date"
    else:
        select_curr = "SELECT * FROM currhist INNER JOIN currency ON currhist.curr_id=currency.id WHERE "
        for cr in curr:
            select_curr += f"curr_id = {cr} OR "
        select_curr = select_curr[:-3] + " ORDER BY date"
    connection = create_connection()
    currs = execute_read_query(connection, select_curr)
    df = pd.DataFrame.from_records(currs)
    df.rename(columns={2: 'Дата', 3: 'Стоимость валюты', 6: 'Обозначение', 7: 'Наименование валюты'}, inplace=True)
    fig = px.line(df, x='Дата', y='Стоимость валюты', color='Обозначение')
    fig.write_html(buffer)
    html_bytes = buffer.getvalue().encode()

    #return buffer;
    return fig
