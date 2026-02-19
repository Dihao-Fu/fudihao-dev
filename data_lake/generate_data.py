"""
Seagate Manufacturing Data Generator
Author: DiHao Fu
Generate realistic manufacturing data for analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("=== Seagate Manufacturing Data Generator ===")

# 1. 生成时间维度数据
dates = pd.date_range(start='2024-01-01', end='2024-03-31', freq='H')
print(f"生成时间数据: {len(dates)} 小时记录")

time_df = pd.DataFrame({
    'timestamp': dates,
    'hour': dates.hour,
    'day': dates.day,
    'month': dates.month,
    'year': dates.year,
    'day_of_week': dates.dayofweek,
    'is_weekday': (dates.dayofweek < 5).astype(int)
})

# 2. 生成设备数据
devices = []
for i in range(1, 21):
    devices.append({
        'device_id': i,
        'device_name': f'Machine_{i:03d}',
        'device_type': np.random.choice(['Assembly', 'Testing', 'Packaging']),
        'location': np.random.choice(['Line_A', 'Line_B', 'Line_C']),
        'install_date': '2023-01-15'
    })

device_df = pd.DataFrame(devices)

# 3. 生成传感器数据（核心）
print("生成传感器数据...")
sensor_data = []

for device in devices:
    device_id = device['device_id']
    base_temp = np.random.uniform(20, 25)
    base_vibration = np.random.uniform(0.1, 0.3)
    
    for ts in dates[:500]:  # 每个设备500小时数据
        # 正常波动
        temp = base_temp + np.random.normal(0, 0.5)
        vibration = base_vibration + np.random.normal(0, 0.05)
        
        # 偶尔异常（模拟故障前兆）
        if np.random.random() < 0.005:  # 0.5%异常率
            temp += np.random.uniform(5, 15)
            vibration *= np.random.uniform(2, 5)
        
        sensor_data.append({
            'timestamp': ts,
            'device_id': device_id,
            'temperature': round(temp, 2),
            'vibration': round(vibration, 4),
            'power_usage': np.random.uniform(1.5, 2.5),
            'status': 'NORMAL' if temp < 35 and vibration < 0.8 else 'WARNING'
        })

sensor_df = pd.DataFrame(sensor_data)
print(f"传感器数据: {len(sensor_df)} 条记录")

# 4. 生成产品质量数据
print("生成产品质量数据...")
products = []
for i in range(1, 1001):
    products.append({
        'product_id': f'HD_{i:06d}',
        'batch_id': f'BATCH_{np.random.randint(1, 11):03d}',
        'production_date': (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 90))).strftime('%Y-%m-%d'),
        'device_id': np.random.randint(1, 21),
        'test_result': np.random.choice(['PASS', 'FAIL'], p=[0.95, 0.05]),
        'read_speed': np.random.normal(200, 20),
        'write_speed': np.random.normal(180, 25),
        'latency': np.random.normal(4.5, 0.8)
    })

product_df = pd.DataFrame(products)

# 5. 创建目录并保存
os.makedirs('data_lake/raw', exist_ok=True)

time_df.to_csv('data_lake/raw/time_dimension.csv', index=False)
device_df.to_csv('data_lake/raw/device_dimension.csv', index=False)
sensor_df.to_csv('data_lake/raw/sensor_fact.csv', index=False)
product_df.to_csv('data_lake/raw/product_quality.csv', index=False)

print("=== 数据生成完成 ===")
print(f"时间维度: {len(time_df)} 行")
print(f"设备维度: {len(device_df)} 行")
print(f"传感器事实: {len(sensor_df)} 行")
print(f"产品质量: {len(product_df)} 行")
print("文件已保存到 data_lake/raw/")
