# @Author : mcyj
# @Time : 2025/1/7 上午9:56

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import mplcursors  # 导入 mplcursors 库
from matplotlib.dates import DateFormatter, date2num  # 用于格式化日期
from matplotlib.widgets import RangeSlider  # 导入范围滑块组件

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

# 计算5日、10日和30日均线
df['5_day_avg'] = df['close'].rolling(window=5).mean()
df['10_day_avg'] = df['close'].rolling(window=10).mean()
df['30_day_avg'] = df['close'].rolling(window=30).mean()

# 创建图表
fig, ax = plt.subplots(figsize=(14, 7))
plt.subplots_adjust(bottom=0.25)  # 为滑块留出空间

# 绘制初始图表
line_close, = ax.plot(df['trade_date'], df['close'], label='Close Price', color='blue')
line_5_day, = ax.plot(df['trade_date'], df['5_day_avg'], label='5-Day Moving Average', color='orange')
line_10_day, = ax.plot(df['trade_date'], df['10_day_avg'], label='10-Day Moving Average', color='green')
line_30_day, = ax.plot(df['trade_date'], df['30_day_avg'], label='30-Day Moving Average', color='red')

# 添加标题和标签
ax.set_title('Yonghui Supermarket Stock Price with Moving Averages')
ax.set_xlabel('Trade Date')
ax.set_ylabel('Price')
ax.legend()

# 格式化横轴日期显示
date_format = DateFormatter('%Y-%m-%d')  # 设置日期格式为年-月-日
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()  # 自动调整横轴日期标签的角度

# 启用 mplcursors 的悬停功能
cursor = mplcursors.cursor(hover=True)


# 自定义悬停显示的内容
@cursor.connect("add")
def on_add(sel):
    # 获取鼠标悬停点的索引，并转换为整数
    index = int(sel.index)
    # 获取对应的日期和价格
    date = df['trade_date'].iloc[index].strftime('%Y-%m-%d')
    close_price = df['close'].iloc[index]
    # 设置悬停显示的内容
    sel.annotation.set_text(f"Date: {date}\nClose Price: {close_price:.2f}")

    # 根据线条颜色设置注解框的背景颜色
    if sel.artist == line_close:
        sel.annotation.get_bbox_patch().set_facecolor('blue')
    elif sel.artist == line_5_day:
        sel.annotation.get_bbox_patch().set_facecolor('orange')
    elif sel.artist == line_10_day:
        sel.annotation.get_bbox_patch().set_facecolor('green')
    elif sel.artist == line_30_day:
        sel.annotation.get_bbox_patch().set_facecolor('red')

    # 设置注解框的透明度
    sel.annotation.get_bbox_patch().set_alpha(0.8)


# 滑块功能
# 创建滑块的位置
ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])  # 滑块的位置和大小
slider = RangeSlider(ax_slider, '', 0, 1, valinit=(0, 1), valstep=0.01)  # 范围滑块，初始范围为 0 到 1

# 初始显示范围
total_days = len(df)
min_days = 15  # 最小显示 15 天


# 滑块回调函数
def update(val):
    # 获取滑块的值（范围）
    start_ratio, end_ratio = val

    # 计算显示范围的起始位置
    start_index = int(start_ratio * (total_days - min_days))
    end_index = int(end_ratio * (total_days - min_days)) + min_days

    # 设置显示范围
    ax.set_xlim(df['trade_date'].iloc[start_index], df['trade_date'].iloc[end_index - 1])
    fig.canvas.draw_idle()  # 重新绘制图表


# 绑定滑块事件
slider.on_changed(update)


# 鼠标滚轮缩放功能
def on_scroll(event):
    ax = event.inaxes
    if ax is None:
        return

    # 获取当前显示范围
    xlim = ax.get_xlim()
    current_range = xlim[1] - xlim[0]  # 当前显示的天数范围

    # 计算新的显示范围
    scale_factor = 1.1 if event.button == 'up' else 0.9  # 滚轮向上放大，向下缩小
    new_range = current_range * scale_factor

    # 限制显示范围在 15 到总数据量之间
    if new_range < min_days:
        new_range = min_days
    elif new_range > total_days:
        new_range = total_days

    # 计算新的 xlim
    center = (xlim[0] + xlim[1]) / 2  # 当前显示范围的中心点
    new_xlim = (center - new_range / 2, center + new_range / 2)

    # 限制 xlim 在数据的有效范围内
    min_date = date2num(df['trade_date'].min())
    max_date = date2num(df['trade_date'].max())
    if new_xlim[0] < min_date:
        new_xlim = (min_date, min_date + new_range)
    if new_xlim[1] > max_date:
        new_xlim = (max_date - new_range, max_date)

    # 设置新的 xlim
    ax.set_xlim(new_xlim)

    # 更新滑块的范围
    start_ratio = (new_xlim[0] - min_date) / (max_date - min_date)
    end_ratio = (new_xlim[1] - min_date) / (max_date - min_date)
    slider.set_val((start_ratio, end_ratio))  # 更新滑块的范围

    fig.canvas.draw_idle()  # 重新绘制图表


# 绑定滚轮事件
fig.canvas.mpl_connect('scroll_event', on_scroll)

# 显示图表
plt.show()