import pandas as pd
from sqlalchemy import create_engine

# 读取CSV文件
csv_file_path = '../stock_csv/tushare_daily_20250108090207.csv'  # 替换为您的CSV文件路径
df = pd.read_csv(csv_file_path)

# 由于CSV文件没有stock_name列，我们需要添加这一列
df['stock_name'] = '永辉超市'

# 创建数据库连接引擎
# 请根据实际情况替换用户名、密码、主机和数据库名
engine = create_engine('mysql://root:@127.0.0.1:3306/stock?charset=utf8&use_unicode=1')

# 将DataFrame写入MySQL数据库
# table参数指定要写入的表名，if_exists参数指定如果表已存在时的行为（'fail', 'replace', 'append'）
def write_csvdata_to_db(df, engine):
    try:
        df.to_sql('stock_daily', con=engine, if_exists='append', index=False)
        print("数据已成功插入到stock_daily表中")
    except Exception as e:
        print(f"发生错误: {e}")

# 定义查询语句
query = """
SELECT trade_date, open, high, low, close
FROM stock_daily
WHERE stock_name = '永辉超市'
"""

if __name__ == '__main__':
    write_csvdata_to_db(df, engine)
    # df = pd.read_sql_query(query, engine)
    # total_trade_date_count = df['trade_date'].count()
    # print(f"查询到{total_trade_date_count}条记录")