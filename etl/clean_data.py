"""
ETL Pipeline: Clean and transform raw data
Author: DiHao Fu
"""

import pandas as pd
import numpy as np
import os

print("=== ETL数据清洗管道 ===")

# 创建目录
os.makedirs('data_lake/bronze', exist_ok=True)
os.makedirs('data_lake/silver', exist_ok=True)

# 1. 清洗传感器数据
print("1. 清洗传感器数据...")
sensor_raw = pd.read_csv('data_lake/raw/sensor_fact.csv')

sensor_cleaned = sensor_raw.copy()
sensor_cleaned['timestamp'] = pd.to_datetime(sensor_cleaned['timestamp'])

# 处理异常值
sensor_cleaned = sensor_cleaned[
    (sensor_cleaned['temperature'] >= 0) & 
    (sensor_cleaned['temperature'] <= 100) &
    (sensor_cleaned['vibration'] >= 0) &
    (sensor_cleaned['vibration'] <= 10)
]

# 添加分类列
sensor_cleaned['temp_category'] = pd.cut(
    sensor_cleaned['temperature'],
    bins=[0, 30, 40, 50, 100],
    labels=['正常', '注意', '警告', '危险']
)

sensor_cleaned['vib_category'] = pd.cut(
    sensor_cleaned['vibration'],
    bins=[0, 0.3, 0.6, 1.0, 10],
    labels=['平稳', '轻微', '明显', '严重']
)

sensor_cleaned.to_csv('data_lake/bronze/sensor_cleaned.csv', index=False)
print(f"  保存清洗后数据: {len(sensor_cleaned)} 行")

# 2. 清洗产品质量数据
print("2. 清洗产品质量数据...")
quality_raw = pd.read_csv('data_lake/raw/product_quality.csv')

quality_cleaned = quality_raw.copy()
quality_cleaned['production_date'] = pd.to_datetime(quality_cleaned['production_date'])

# 移除无效数据
quality_cleaned = quality_cleaned[
    (quality_cleaned['read_speed'] > 0) &
    (quality_cleaned['write_speed'] > 0) &
    (quality_cleaned['latency'] > 0)
]

# 计算质量得分
quality_cleaned['quality_score'] = (
    quality_cleaned['read_speed'] / 250 * 0.4 +
    quality_cleaned['write_speed'] / 220 * 0.4 +
    (10 - quality_cleaned['latency']) / 10 * 0.2
)

quality_cleaned.to_csv('data_lake/bronze/quality_cleaned.csv', index=False)
print(f"  保存清洗后数据: {len(quality_cleaned)} 行")

# 3. 创建聚合数据
print("3. 创建聚合数据...")

# 设备每日统计
daily_stats = sensor_cleaned.groupby(['device_id', sensor_cleaned['timestamp'].dt.date]).agg({
    'temperature': ['mean', 'max', 'min'],
    'vibration': ['mean', 'max'],
    'power_usage': 'mean'
}).round(3)

daily_stats.columns = ['_'.join(col).strip() for col in daily_stats.columns.values]
daily_stats = daily_stats.reset_index()
daily_stats.to_csv('data_lake/silver/daily_device_stats.csv', index=False)

print("=== ETL处理完成 ===")
