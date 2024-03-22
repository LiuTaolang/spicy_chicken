import pandas as pd

import tools_method as tm
from fund import Fund

fund_list = tm.get_fund_list()
result = {
    'code': [],
    'name': [],
    'type': [],
    'start_date': [],
    'start_price': [],
    'current_date': [],
    'current_price': [],
    'high_date': [],
    'high_price': [],
    'low_date': [],
    'low_price': [],
    'current/start': [],
    'current/high': [],
    'current/low': []
}

for index, row in fund_list.iterrows():
    fund = Fund(row=row)
    df = fund.hfq_hist
    first_row = df.head(1)
    last_row = df.tail(1)
    max_row = df[df[fund.high] == df[fund.high].max()]
    min_row = df[df[fund.low] == df[fund.low].min()]
    result['code'].append(f"'{fund.code}")
    result['name'].append(fund.name)
    result['type'].append(fund.type)
    
    result['start_date'].append(first_row['日期'].iloc[0])
    start_price = first_row[fund.cls].iloc[0]
    result['start_price'].append(start_price)

    result['current_date'].append(last_row['日期'].iloc[0])
    current_price = last_row[fund.cls].iloc[0]
    result['current_price'].append(current_price)

    result['high_date'].append(max_row['日期'].iloc[0])
    high_price = max_row[fund.high].iloc[0]
    result['high_price'].append(high_price)

    result['low_date'].append(min_row['日期'].iloc[0])
    low_price = min_row[fund.low].iloc[0]
    result['low_price'].append(low_price)

    result['current/start'].append(current_price/start_price)
    result['current/high'].append(current_price/high_price)
    result['current/low'].append(current_price/low_price)
    
    if index == 5:
        break

df = pd.DataFrame.from_dict(result)
df_sorted = df.sort_values(by='current/high', ascending=True)
df_sorted.to_csv('spicy_chicken.csv')