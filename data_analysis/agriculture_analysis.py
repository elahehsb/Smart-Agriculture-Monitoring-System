import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load data
data = pd.read_csv('sensor_data.csv')

# Preprocess data
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')
data.set_index('timestamp', inplace=True)

# Visualization
plt.figure(figsize=(12, 6))
sns.lineplot(data=data, x='timestamp', y='temperature', label='Temperature')
sns.lineplot(data=data, x='timestamp', y='humidity', label='Humidity')
sns.lineplot(data=data, x='timestamp', y='soil_moisture', label='Soil Moisture')
plt.title('Sensor Data Over Time')
plt.show()

# Feature Engineering
data['day_of_year'] = data.index.dayofyear

# Train/Test Split
features = ['day_of_year']
X = data[features]
y = data['soil_moisture']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('R2 Score:', r2_score(y_test, y_pred))

# Plot predictions
plt.figure(figsize=(10, 6))
plt.scatter(X_test['day_of_year'], y_test, color='black', label='Actual')
plt.scatter(X_test['day_of_year'], y_pred, color='blue', label='Predicted')
plt.title('Soil Moisture Prediction')
plt.xlabel('Day of Year')
plt.ylabel('Soil Moisture')
plt.legend()
plt.show()
