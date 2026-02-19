"""
Simple predictive maintenance model
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

print("训练预测模型...")

# 加载数据
df = pd.read_csv('data_lake/bronze/sensor_cleaned.csv')

# 准备特征
features = ['temperature', 'vibration', 'power_usage']
X = df[features].fillna(0)
y = (df['status'] == 'WARNING').astype(int)  # 1表示警告

# 训练简单模型
model = RandomForestClassifier(n_estimators=10)
model.fit(X[:1000], y[:1000])

# 保存模型
joblib.dump(model, 'ml/failure_predictor.pkl')
print("模型已保存")
