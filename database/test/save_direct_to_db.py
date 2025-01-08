# @Author : mcyj
# @Time : 2025/1/8 上午8:38

import pandas as pd
from sqlalchemy import create_engine

# 读取CSV文件
csv_file_path = '../stock_csv/tushare_daily_20250107085416.csv'  # 替换为您的CSV文件路径
df = pd.read_csv(csv_file_path)

# 由于CSV文件没有stock_name列，我们需要添加这一列
df['stock_name'] = '永辉超市'
df['trade_date'] = '2025-01-07'
df['vol'] = '5690287'
df['open'] = '5.85'
df['high'] = '6.05'
df['low'] = '5.69'
df['close'] = '5.97'
df['pct_chg'] = '0.1678'

# 创建数据库连接引擎
# 请根据实际情况替换用户名、密码、主机和数据库名
engine = create_engine('mysql://root:@127.0.0.1:3306/stock?charset=utf8&use_unicode=1')
