import pandas as pd
import os

os.makedirs("dataset", exist_ok=True)

files = {
    "cleaned_air.csv": "raw_data/air_quality_data.csv",
    "cleaned_bus.csv": "raw_data/bus_routes.csv",
    "cleaned_commuter.csv": "raw_data/commuter_patterns.csv",
    "cleaned_traffic.csv": "raw_data/traffic_flow_data.csv",
    "cleaned_road.csv": "raw_data/road_segments.csv",
    "cleaned_weather.csv": "raw_data/weather_data.csv"
}

for output, path in files.items():
    df = pd.read_csv(path)

    df.drop_duplicates(inplace=True)

    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()

    df.fillna(method="ffill", inplace=True)

    save_path = f"dataset/{output}"
    df.to_csv(save_path, index=False)

print("All cleaned files saved.")