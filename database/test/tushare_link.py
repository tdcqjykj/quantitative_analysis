# @Author : mcyj
# @Time : 2025/1/6 下午4:32

import pandas as pd
import tushare as ts
from sqlalchemy import create_engine

ts.set_token('d499c0996f2683e29f260b0e62df6b67e33c234b073d361736e18c87')  # 设置Tushare API Token
pro = ts.pro_api()  # 初始化Tushare Pro API

engine_ts = create_engine('mysql://root:@127.0.0.1:3306/stock?charset=utf8&use_unicode=1')

# 获取指定股票的历史行情数据
def get_stock_daily_data(ts_code, start_date, end_date, stock_name):
    try:
        # 使用 Tushare Pro API 拉取数据
        # 拉取数据
        df = pro.daily(**{"ts_code": ts_code,"trade_date": "","start_date": start_date,
                            "end_date": end_date,"offset": 0,"limit": ""},
                       fields=["trade_date","open","high","low","close","pct_chg","vol"])

        df['stock_name'] = stock_name
        return df
    except Exception as e:
        print(f"Error fetching data for {ts_code}: {e}")
        return pd.DataFrame()  # 返回空 DataFrame 以避免后续代码出错

# 将数据写入数据库
def write_data_to_db(df, table_name):
    try:
        df.to_sql(table_name, engine_ts, index=False, if_exists='append')
    except Exception as e:
        print(f"Error writing data to database: {e}")


if __name__ == '__main__':
    start_date = '20240101'  # 开始日期
    end_date = '20250106'  # 结束日期
    ts_code = '601933.SH'  # 永辉超市的股票代码
    stock_name = '永辉超市'  # 永辉超市的股票名称
    # 获取数据
    df = get_stock_daily_data(ts_code, start_date, end_date,stock_name)

    # 写入数据库
    write_data_to_db(df, 'stock_daily')

    # 打印前几行数据以验证
    print(df.head())
