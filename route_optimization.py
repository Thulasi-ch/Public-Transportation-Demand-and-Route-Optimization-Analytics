import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Create folders
os.makedirs("output", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Load data
df = pd.read_csv("dataset/cleaned_road.csv")

# Clean numeric columns
df["length"] = pd.to_numeric(df["length"], errors="coerce")
df["speed_limit"] = pd.to_numeric(df["speed_limit"], errors="coerce")
df["lanes"] = pd.to_numeric(df["lanes"], errors="coerce")

df.dropna(inplace=True)

# Travel time estimate
df["travel_time"] = df["length"] / df["speed_limit"]

# Optimization score:
# lower time better, more lanes better
df["route_score"] = (1 / df["travel_time"]) * df["lanes"]

# Top 10 routes
best = df.sort_values(by="route_score", ascending=False).head(10).copy()

# Round values
best["length"] = best["length"].round(2)
best["travel_time"] = best["travel_time"].round(2)
best["route_score"] = best["route_score"].round(2)

# Rename columns
best = best.rename(columns={
    "source": "From",
    "target": "To",
    "length": "Distance",
    "speed_limit": "Speed Limit",
    "lanes": "Lanes",
    "travel_time": "Travel Time",
    "route_score": "Score"
})

# Save output
best.to_csv("output/optimized_routes.csv", index=False)

# -------- Chart --------
plt.figure(figsize=(12,6))
plt.bar(best["From"].astype(str), best["Score"])
plt.title("Top Optimized Routes")
plt.xlabel("Source Node")
plt.ylabel("Route Efficiency Score")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("charts/optimized_routes.png")
plt.close()

print("Route optimization completed successfully.")
print(best)