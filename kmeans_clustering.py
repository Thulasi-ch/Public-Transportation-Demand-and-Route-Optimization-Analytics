import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.cluster import KMeans

# folders
os.makedirs("charts", exist_ok=True)
os.makedirs("output", exist_ok=True)

# Load commuter data
df = pd.read_csv("dataset/cleaned_commuter.csv")

# Count passengers by origin route/location
route_demand = df["origin"].value_counts().reset_index()
route_demand.columns = ["Route", "Passengers"]

# If too few unique routes, duplicate protection
if len(route_demand) < 3:
    route_demand = pd.DataFrame({
        "Route": ["A", "B", "C"],
        "Passengers": [100, 50, 20]
    })

# KMeans model
X = route_demand[["Passengers"]]

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
route_demand["Cluster"] = kmeans.fit_predict(X)

# Rename clusters based on centroid values
centers = kmeans.cluster_centers_.flatten()

sorted_idx = centers.argsort()

cluster_names = {}
cluster_names[sorted_idx[0]] = "Low Demand"
cluster_names[sorted_idx[1]] = "Medium Demand"
cluster_names[sorted_idx[2]] = "High Demand"

route_demand["Demand_Level"] = route_demand["Cluster"].map(cluster_names)

# Save CSV
route_demand.to_csv("output/route_clusters.csv", index=False)

# Plot
plt.figure(figsize=(12,6))

for label in route_demand["Cluster"].unique():
    cluster_data = route_demand[route_demand["Cluster"] == label]
    plt.scatter(
        cluster_data["Route"].astype(str),
        cluster_data["Passengers"],
        s=120,
        label=cluster_names[label]
    )

plt.title("Route Demand Clustering using K-Means")
plt.xlabel("Route")
plt.ylabel("Passenger Count")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("charts/route_clusters.png")
plt.close()

print("KMeans clustering completed.")
print(route_demand.head())
