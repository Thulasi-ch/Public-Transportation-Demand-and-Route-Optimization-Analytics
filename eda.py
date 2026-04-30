import pandas as pd
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("dataset/cleaned_commuter.csv")

df["departure_time"] = pd.to_datetime(df["departure_time"])
df["arrival_time"] = pd.to_datetime(df["arrival_time"])

df["travel_minutes"] = (
    df["arrival_time"] - df["departure_time"]
).dt.total_seconds() / 60

plt.figure(figsize=(10,5))
plt.hist(df["travel_minutes"], bins=20)
plt.title("Travel Time Analysis")
plt.xlabel("Minutes")
plt.ylabel("Passengers")
plt.tight_layout()
plt.savefig("charts/travel_time.png")
plt.close()