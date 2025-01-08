# @Author : mcyj
# @Time : 2025/1/8 上午8:38

import pandas as pd
from sqlalchemy import create_engine

# 创建一个包含一行数据的 DataFrame
data = {
    'stock_name': ['永辉超市'],
    'trade_date': ['2025-01-08'],
    'open': [5.95],
    'high': [6.09],
    'low': [5.74],
    'close': [5.94],
    'pct_chg': [-0.5025],
    'vol': [5049431.55]
}
df = pd.DataFrame(data)

# 创建数据库连接引擎
# 请根据实际情况替换用户名、密码、主机和数据库名
engine = create_engine('mysql://root:@127.0.0.1:3306/stock?charset=utf8&use_unicode=1')

try:
    df.to_sql('stock_daily', con=engine, if_exists='append', index=False)
    print("数据已成功插入到stock_daily表中")
except Exception as e:
    print(f"发生错误: {e}")