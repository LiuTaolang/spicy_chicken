import akshare as ak
import pandas as pd
 
import tools_method as tm

class Fund():
    """基金类"""
    def __init__(self, row, suffix="") -> None:
        """初始化属性 code, update_flag"""
        self.code = row['code']
        self.name = row['name']
        self.type = row['type']
        self.__filename = f"{tm.cache_path}{self.code}{self.type}.json"
        self.__suffix = suffix
        self.cls = self.__set_cls_index()
        self.high = self.__set_high_index()
        self.low = self.__set_low_index()
        self.hfq_hist = self.__set_hfq_history()
        self.__set_creation_date()

    def __set_cls_index(self):
        """设置历史数据中的收盘价列名"""
        cls_index = {'etf': '收盘', 'lof': '收盘', 'onshore': '累计净值',
                     'open': '累计净值', 'index':'累计净值'}
        return f"{cls_index[self.type]}_{self.__suffix}"

    def __set_high_index(self):
        """设置历史数据中的当日最高价列名"""
        high_index = {'etf': '最高', 'lof': '最高', 'onshore': '累计净值',
                'open': '累计净值', 'index':'累计净值'}
        return f"{high_index[self.type]}_{self.__suffix}"

    def __set_low_index(self):
        """设置历史数据中的当日最低价列名"""
        low_index = {'etf': '最低', 'lof': '最低', 'onshore': '累计净值',
                'open': '累计净值', 'index':'累计净值'}
        return f"{low_index[self.type]}_{self.__suffix}"

    def __reset_date_column_format(self, df: pd.DataFrame):
        """重置日期列格式"""
        temp = {'etf': '日期', 'lof': '日期', 'onshore': '净值日期',
                'open': '净值日期', 'index': '净值日期'}
        dt_index = temp[self.type]
        df[dt_index] = pd.to_datetime(df[dt_index], format='%Y-%m-%d')
        df[dt_index] = df[dt_index].dt.strftime('%Y-%m-%d')
        return df

    def __reset_column_name(self, df: pd.DataFrame):
        """重置列名"""
        df.columns = [f"{col}_{self.__suffix}" for col in df.columns]
        if self.type in ['etf', 'lof']:
            return df.rename(columns={f"日期_{self.__suffix}": '日期'})
        elif self.type in ['open', 'onshore', 'index']:
            return df.rename(columns={f'净值日期_{self.__suffix}': '日期'})
        else:
            raise Exception(f"Could not handle this type {self.type}.")

    def __set_hfq_history(self):
        """获取基金后复权历史数据"""
        # 如果文件不是当天生成的，先更新再读取。
        if tm.check_update(self.__filename):
            temp_df = self.__update_hfq_history()
            temp_df = self.__reset_date_column_format(temp_df)
            temp_df.to_json(self.__filename)
        else:
            temp_df = pd.read_json(self.__filename)
        return self.__reset_column_name(temp_df)

    def __update_hfq_history(self):
        """更新基金后复权历史数据"""
        if self.type=='etf':
            return ak.fund_etf_hist_em(symbol=self.code, period="daily", 
                        start_date="19900101", end_date="20900101", adjust="hfq")
        elif self.type=='lof':
            return ak.fund_lof_hist_em(symbol=self.code, period="daily", 
                        start_date="19900101", end_date="20900101", adjust="hfq")
        elif self.type == 'index':
            return ak.fund_open_fund_info_em(symbol=self.code, 
                                                    indicator="累计净值走势")
        elif self.type=='open':
            return ak.fund_open_fund_info_em(symbol=self.code, 
                                                    indicator="累计净值走势")
        elif self.type=='onshore':
            return ak.fund_etf_fund_info_em(fund=self.code, 
                                    start_date="19900101", end_date="20900101")
        else:
            raise Exception(f"could not handle this type {self.type}!")

    def __set_creation_date(self):
        """获取基金的成立日期"""
        self.creation_date = self.hfq_hist['日期'].iloc[0]