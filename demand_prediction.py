import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error
import os

# Create folders
os.makedirs("output", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Load data
df = pd.read_csv("dataset/cleaned_commuter.csv")

# Convert time
df["departure_time"] = pd.to_datetime(df["departure_time"], errors="coerce")

# Extract hour
df["hour"] = df["departure_time"].dt.hour

# Remove null rows
df = df.dropna(subset=["hour"])

# Actual hourly passenger demand
hourly = df.groupby("hour").size().reset_index(name="Passengers")

# Features
X = hourly[["hour"]]
y = hourly["Passengers"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Predict existing hours
y_pred = model.predict(X)

# Metrics
r2 = r2_score(y, y_pred)
mae = mean_absolute_error(y, y_pred)

# Predict future 24 hours
future = pd.DataFrame({"hour": range(24)})
future["Predicted_Passengers"] = model.predict(future[["hour"]]).round().astype(int)
future["Predicted_Passengers"] = future["Predicted_Passengers"].clip(lower=0)

# Save csv
future.to_csv("output/predicted_demand.csv", index=False)

# ---------------- Chart ----------------
plt.figure(figsize=(12,6))

# Actual
plt.scatter(hourly["hour"], hourly["Passengers"], s=80, label="Actual Demand")

# Predicted line
plt.plot(future["hour"], future["Predicted_Passengers"], linewidth=2, label="Predicted Demand")

plt.title("24-Hour Passenger Demand Forecast")
plt.xlabel("Hour of Day")
plt.ylabel("Passengers")
plt.xticks(range(24))
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig("charts/demand_forecast.png")
plt.close()

# Print metrics
print("Demand prediction completed.")
print(f"R2 Score: {r2:.2f}")
print(f"MAE: {mae:.2f}")