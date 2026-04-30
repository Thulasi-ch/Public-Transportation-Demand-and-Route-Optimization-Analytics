import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Create folders
os.makedirs("output", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Load data
commuter = pd.read_csv("dataset/cleaned_commuter.csv")
bus = pd.read_csv("dataset/cleaned_bus.csv")

# Total passengers observed
total_passengers = len(commuter)

# Use actual route capacity
bus["capacity"] = pd.to_numeric(bus["capacity"], errors="coerce")
bus = bus.dropna(subset=["capacity"])

# Capacity share
bus["capacity_share"] = bus["capacity"] / bus["capacity"].sum()

# Estimated passengers per route
bus["Passengers"] = (bus["capacity_share"] * total_passengers).round().astype(int)

# Recommended buses assuming 50 passengers per bus
bus["Recommended_Buses"] = np.ceil(bus["Passengers"] / 50).astype(int)

# Final table
result = bus[["route_id", "Passengers", "Recommended_Buses"]].copy()
result.columns = ["Route", "Passengers", "Recommended_Buses"]

# Save CSV
result.to_csv("output/bus_recommendation.csv", index=False)

# ---------------- Chart ----------------
plt.figure(figsize=(12,6))
plt.bar(result["Route"].astype(str), result["Recommended_Buses"])
plt.title("Bus Allocation Recommendations")
plt.xlabel("Route ID")
plt.ylabel("Recommended Buses")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/bus_allocation.png")
plt.close()

print("Bus allocation completed.")
print(result)