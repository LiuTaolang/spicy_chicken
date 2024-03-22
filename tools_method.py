import os
import datetime

import akshare as ak
import pandas as pd

cache_path = '../cache/'

def check_update(filename):
    try:
        mtime = os.stat(filename).st_mtime
        mtime_dt = datetime.date.fromtimestamp(mtime)
        return True if mtime_dt < datetime.date.today() else False
    except FileNotFoundError:
        return True
    
def get_fund_list() -> pd.DataFrame:
    """读取本地基金清单文件"""
    filename = f"{cache_path}fund_list.json"
    # 如果清单文件不是当天生成的，先更新再读取。
    if check_update(filename):
        temp_df = __update_fund_list(filename)
        temp_df.to_json(filename)
    else:
        temp_df = pd.read_json(filename, dtype={'code': str})
    return temp_df

def __update_fund_list(filename) -> pd.DataFrame:
    """通过 akshare 更新数据"""
    fund_real_time = {
        'index': ak.fund_info_index_em(),
        'etf': ak.fund_etf_spot_em(),
        'lof': ak.fund_lof_spot_em(),
        'open': ak.fund_open_fund_daily_em(),
        # 'money': ak.fund_money_fund_daily_em(),
        'onshore': ak.fund_etf_fund_daily_em(),
    }
    col_name = {
        'etf': ['代码', '名称'],
        'lof': ['代码', '名称'],
        'index': ['基金代码', '基金名称'],
        'open': ['基金代码', '基金简称'],
        # 'money': ['基金代码', '基金简称'],
        'onshore': ['基金代码', '基金简称'],
    }
    for k, v in fund_real_time.items():
        try:
            v['type'] = k
        except TypeError:
            print(f"{k} 类型查不到实时数据，请检查接口。")
            continue
        col = col_name[k]
        v.rename(columns={col[0]: 'code', col[1]: 'name'}, inplace=True)
        try:
            df = pd.concat([df, v[['code', 'name', 'type']]], ignore_index=True)
        except NameError:
            df = v[['code', 'name', 'type']]
    df = df.drop_duplicates(subset='code', keep='first')
    return df