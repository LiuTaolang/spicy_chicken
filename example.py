import threading
import time

import pandas as pd

import tools_method as tm
from fund import Fund

start_time = time.time()
# 获取基金列表
fund_list = tm.get_fund_list()

# 初始化结果字典
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
    'current/low': [],
    'median_of_min_10%': [],
    'current/min10%': [],
}

# 定义处理每行数据的函数
def process_row(row, index, result):
    fund = Fund(row=row)
    df = fund.hfq_hist
    # df = df.loc[df['日期'] >= '2019-01-01']
    first_row = df.head(1)
    last_row = df.tail(1)
    max_row = df[df[fund.high] == df[fund.high].max()]
    min_row = df[df[fund.low] == df[fund.low].min()]

    # 获取最小 10% 的记录的平均数
    sorted_df = df.sort_values(by=fund.low)
    top_10_percent_count = int(len(sorted_df) * 0.01) + 1
    top_10_percent_df = sorted_df.iloc[:top_10_percent_count]
    median_of_top_10_percent = top_10_percent_df[fund.low].median()

    # 锁定字典以更新结果
    with lock:
        result['code'].append(f'{fund.code}')
        result['name'].append(fund.name)
        result['type'].append(fund.type)
        result['start_date'].append(first_row['日期'].iloc[0])
        result['start_price'].append(first_row[fund.cls].iloc[0])
        result['current_date'].append(last_row['日期'].iloc[0])
        result['current_price'].append(last_row[fund.cls].iloc[0])
        result['high_date'].append(max_row['日期'].iloc[0])
        result['high_price'].append(max_row[fund.high].iloc[0])
        result['low_date'].append(min_row['日期'].iloc[0])
        result['low_price'].append(min_row[fund.low].iloc[0])
        result['current/start'].append(last_row[fund.cls].iloc[0] / first_row[fund.cls].iloc[0])
        result['current/high'].append(last_row[fund.cls].iloc[0] / max_row[fund.high].iloc[0])
        result['current/low'].append(last_row[fund.cls].iloc[0] / min_row[fund.low].iloc[0])
        result['median_of_min_10%'].append(median_of_top_10_percent)
        result['current/min10%'].append(last_row[fund.cls].iloc[0] / median_of_top_10_percent)


# 创建一个线程锁
lock = threading.Lock()

# 创建线程列表
threads = []

# 遍历基金列表并创建线程
for index, row in fund_list.iterrows():
    thread = threading.Thread(target=process_row, args=(row, index, result))
    threads.append(thread)
    thread.start()

    # 限制为处理前500行
    # if index == 500:
    #     break

# 等待所有线程完成
for thread in threads:
    thread.join()

# 将结果转换为 DataFrame 并排序
df = pd.DataFrame.from_dict(result)
df_sorted = df.sort_values(by='current/high', ascending=True)

# 保存到 CSV 文件
df_sorted.to_csv('spicy_chicken.csv')

end_time = time.time()
print(f"耗时：{end_time - start_time}秒")