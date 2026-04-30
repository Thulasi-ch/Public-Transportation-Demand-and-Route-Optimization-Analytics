import pandas as pd
import os

files = {
    "air": "raw_data/air_quality_data.csv",
    "bus": "raw_data/bus_routes.csv",
    "commuter": "raw_data/commuter_patterns.csv",
    "traffic": "raw_data/traffic_flow_data.csv",
    "road": "raw_data/road_segments.csv",
    "weather": "raw_data/weather_data.csv"
}

for name, path in files.items():
    df = pd.read_csv(path)
    print(f"\n{name.upper()} DATA")
    print(df.head())
    print(df.shape)
    print(df.columns)