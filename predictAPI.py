#!/usr/bin/python3
# -*- coding: utf-8 -*


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error

from pycaret.regression import *
import plotly.express as px

def read_data(filename):
    data = pd.read_excel(filename)
    data["data"] = pd.to_datetime(data['data'], dayfirst=True)
    data.set_index("data", inplace = True)
    data.sort_values("data", inplace = True)
    return data


# функция для построения прогноза моделью

def predict(end_date, currency):
    """end_date in format  %d, %b %Y' (for example 2022-11-20)
        currency - name of currency (monet) ("USD", "EUR", "JPY", "CNY", "GBP")
    """
    
    data = pd.read_csv(f"data/preprocessed/{currency}_df.csv", parse_dates = ["data"], dayfirst = True, 
                       index_col = ["data"])
    model = load_model(f'models/{currency}_model')
    all_dates = pd.date_range(start='2022-11-19', end = end_date, freq = 'D')
    #dates_all = data.index.append(all_dates)
    
    # create empty dataframe
    score_df = pd.DataFrame()
    # add columns to dataset
    score_df['дата'] = all_dates
    score_df['Месяц'] = [i.month for i in score_df['дата']]
    score_df['День недели'] = [i.dayofweek for i in score_df['дата']]
    score_df['День месяца'] = [i.day for i in score_df['дата']]
    p = predict_model(model, data=score_df)
    score_df_n = pd.concat([score_df["дата"],p], axis = 1) 
    data_reset = data.reset_index()
    data_reset.columns = ['дата', 'Курс', 'Месяц', 'День недели', 'День месяца']
    #data_reset_all = data_reset.append(pd.DataFrame(data = score_df_n.дата[122:]))
    data_reset_all = data_reset.append(pd.DataFrame(data = score_df_n.дата))
    final_df = pd.merge(data_reset_all, score_df_n, how = 'left', left_on=['дата', ], right_on = ['дата'])
    final_df.columns = (['дата', 'Факт', 'Месяц_x', 'День недели_x', 'День месяца_x', 'Месяц_y',
       'День недели_y', 'День месяца_y', 'Прогноз моделью'])
    
    
    fig = px.line(final_df, x="дата", y=["Факт", "Прогноз моделью"], 
        title=f"Прогноз цены {currency}",).update_layout(yaxis={"title": "Курс, руб."}, legend={"title":"Дата"})
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.show()
    
    return final_df

