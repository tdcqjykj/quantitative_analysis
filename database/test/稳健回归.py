# @Author : mcyj
# @Time : 2025/1/7 上午11:51

import pandas as pd
from sqlalchemy import create_engine
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.robust.robust_linear_model import RLM

# 数据库连接配置
db_config = {
    'user': 'root',  # 用户名
    'password': '',  # 密码为空
    'host': '127.0.0.1',  # 主机地址
    'port': '3306',  # 端口
    'database': 'stock'  # 数据库名称
}

# 创建数据库连接
engine = create_engine(
    f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?charset=utf8&use_unicode=1")

# 查询数据
query = "SELECT * FROM stock_daily WHERE stock_name = '永辉超市' ORDER BY trade_date"
df = pd.read_sql(query, engine)

# 将trade_date列转换为日期格式
df['trade_date'] = pd.to_datetime(df['trade_date'])

# 特征变量
features = ['open', 'high', 'low', 'vol']

# 预测收盘价
X_close = df[features]
X_close = sm.add_constant(X_close)  # 添加常数项
y_close = df['close']  # 目标变量为收盘价

# 预测最高价
X_high = df[features]
X_high = sm.add_constant(X_high)  # 添加常数项
y_high = df['high']  # 目标变量为最高价

# 预测最低价
X_low = df[features]
X_low = sm.add_constant(X_low)  # 添加常数项
y_low = df['low']  # 目标变量为最低价

# 划分训练集和测试集
train_size = int(len(df) * 0.8)
X_train_close, X_test_close = X_close[:train_size], X_close[train_size:]
y_train_close, y_test_close = y_close[:train_size], y_close[train_size:]

X_train_high, X_test_high = X_high[:train_size], X_high[train_size:]
y_train_high, y_test_high = y_high[:train_size], y_high[train_size:]

X_train_low, X_test_low = X_low[:train_size], X_low[train_size:]
y_train_low, y_test_low = y_low[:train_size], y_low[train_size:]

# 构建普通最小二乘回归模型（预测收盘价）
ols_model_close = sm.OLS(y_train_close, X_train_close)
ols_result_close = ols_model_close.fit()

# 输出模型摘要
print("普通最小二乘回归模型（预测收盘价）摘要:")
print(ols_result_close.summary())

# 预测测试集
y_pred_close = ols_result_close.predict(X_test_close)

# 计算均方误差 (MSE)
mse_close = np.mean((y_pred_close - y_test_close) ** 2)
print(f"普通最小二乘回归模型（预测收盘价）均方误差 (MSE): {mse_close:.4f}")

# 构建稳健回归模型（预测收盘价）
robust_model_close = RLM(y_train_close, X_train_close, M=sm.robust.norms.HuberT())
robust_result_close = robust_model_close.fit()

# 输出稳健回归模型摘要
print("稳健回归模型（预测收盘价）摘要:")
print(robust_result_close.summary())

# 预测测试集
y_pred_robust_close = robust_result_close.predict(X_test_close)

# 计算均方误差 (MSE)
mse_robust_close = np.mean((y_pred_robust_close - y_test_close) ** 2)
print(f"稳健回归模型（预测收盘价）均方误差 (MSE): {mse_robust_close:.4f}")

# 构建普通最小二乘回归模型（预测最高价）
ols_model_high = sm.OLS(y_train_high, X_train_high)
ols_result_high = ols_model_high.fit()

# 输出模型摘要
print("普通最小二乘回归模型（预测最高价）摘要:")
print(ols_result_high.summary())

# 预测测试集
y_pred_high = ols_result_high.predict(X_test_high)

# 计算均方误差 (MSE)
mse_high = np.mean((y_pred_high - y_test_high) ** 2)
print(f"普通最小二乘回归模型（预测最高价）均方误差 (MSE): {mse_high:.4f}")

# 构建稳健回归模型（预测最高价）
robust_model_high = RLM(y_train_high, X_train_high, M=sm.robust.norms.HuberT())
robust_result_high = robust_model_high.fit()

# 输出稳健回归模型摘要
print("稳健回归模型（预测最高价）摘要:")
print(robust_result_high.summary())

# 预测测试集
y_pred_robust_high = robust_result_high.predict(X_test_high)

# 计算均方误差 (MSE)
mse_robust_high = np.mean((y_pred_robust_high - y_test_high) ** 2)
print(f"稳健回归模型（预测最高价）均方误差 (MSE): {mse_robust_high:.4f}")

# 构建普通最小二乘回归模型（预测最低价）
ols_model_low = sm.OLS(y_train_low, X_train_low)
ols_result_low = ols_model_low.fit()

# 输出模型摘要
print("普通最小二乘回归模型（预测最低价）摘要:")
print(ols_result_low.summary())

# 预测测试集
y_pred_low = ols_result_low.predict(X_test_low)

# 计算均方误差 (MSE)
mse_low = np.mean((y_pred_low - y_test_low) ** 2)
print(f"普通最小二乘回归模型（预测最低价）均方误差 (MSE): {mse_low:.4f}")

# 构建稳健回归模型（预测最低价）
robust_model_low = RLM(y_train_low, X_train_low, M=sm.robust.norms.HuberT())
robust_result_low = robust_model_low.fit()

# 输出稳健回归模型摘要
print("稳健回归模型（预测最低价）摘要:")
print(robust_result_low.summary())

# 预测测试集
y_pred_robust_low = robust_result_low.predict(X_test_low)

# 计算均方误差 (MSE)
mse_robust_low = np.mean((y_pred_robust_low - y_test_low) ** 2)
print(f"稳健回归模型（预测最低价）均方误差 (MSE): {mse_robust_low:.4f}")

# 获取今天的特征数据
today_features = df[features].iloc[-1].values.reshape(1, -1)
# 手动添加常数项
today_features = np.column_stack((np.ones(today_features.shape[0]), today_features))

# 预测今天的收盘价、最高价和最低价
today_pred_close_ols = ols_result_close.predict(today_features)
today_pred_close_robust = robust_result_close.predict(today_features)

today_pred_high_ols = ols_result_high.predict(today_features)
today_pred_high_robust = robust_result_high.predict(today_features)

today_pred_low_ols = ols_result_low.predict(today_features)
today_pred_low_robust = robust_result_low.predict(today_features)

print(f"普通最小二乘回归模型预测今天永辉超市的收盘价: {today_pred_close_ols[0]:.4f}")
print(f"稳健回归模型预测今天永辉超市的收盘价: {today_pred_close_robust[0]:.4f}")
print(f"普通最小二乘回归模型预测今天永辉超市的最高价: {today_pred_high_ols[0]:.4f}")
print(f"稳健回归模型预测今天永辉超市的最高价: {today_pred_high_robust[0]:.4f}")
print(f"普通最小二乘回归模型预测今天永辉超市的最低价: {today_pred_low_ols[0]:.4f}")
print(f"稳健回归模型预测今天永辉超市的最低价: {today_pred_low_robust[0]:.4f}")
