import pandas as pd
import numpy as np


def prefilter_items(data,take_n_popular=5000):

    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб.
    data['price'] = data['sales_value'] / (np.maximum(data['quantity'], 1))
    data = data[data['price'] > 2]

    # Уберем слишком дорогие товары
    data = data[data['price'] < 50]

    # Уберем самые популярные товары (их и так купят), одновременно убирая товары без продаж
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)

    top = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
    zero = popularity.loc[popularity['n_sold'] == 0,'item_id'].to_list()

    data.loc[~data['item_id'].isin(top),'item_id'] = 999999
    data.loc[~data['item_id'].isin(zero),'item_id'] = 999998

    return data

def postfilter_items(user_id, recommednations):
    pass
