import streamlit as st
import pandas as pd
import os
from pathlib import Path

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Public Transportation Demand and Route Optimization Analytics",
    page_icon="🚌",
    layout="wide"
)

# ---------------- PATH SETUP ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CHARTS_DIR = BASE_DIR
DATASET_DIR = BASE_DIR
OUTPUT_DIR = BASE_DIR

# ---------------- HELPERS ----------------
def show_image(filename, title):
    path = os.path.join(CHARTS_DIR, filename)

    if os.path.exists(path):
        st.image(path, use_container_width=True, caption=title)
    else:
        st.warning(f"{filename} not found.")


def load_csv(filename):
    path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(path):
        return pd.read_csv(path)

    return None
# ---------------- TITLE ----------------
st.title("🚌 Public Transportation Demand and Route Optimization Analytics")
st.markdown("Interactive Smart Dashboard for Urban Mobility Insights")

# ---------------- SIDEBAR ----------------
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "EDA Insights",
        "Demand Prediction",
        "Route Optimization",
        "Bus Allocation",
        "Reports & Downloads"
    ]
)

# ======================================================
# OVERVIEW
# ======================================================
if page == "Overview":

    st.subheader("📌 Project Overview")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Raw Datasets Used", "6")

    with c2:
        st.metric("Commuter Records", "1000+")

    with c3:
        st.metric("Road Segments", "200")

    st.markdown("---")

    st.markdown("""
### Objectives Achieved

✅ Analyze passenger demand patterns  
✅ Identify peak travel hours  
✅ Detect congested routes  
✅ Recommend bus allocation  
✅ Optimize shortest efficient routes  
✅ Forecast future passenger demand  
✅ Build interactive dashboard  

### Real Benefits

🚍 Reduce waiting time  
🚦 Lower congestion  
📈 Better planning  
💰 Lower operational cost  
🙂 Improve passenger satisfaction
""")

# ======================================================
# EDA
# ======================================================
elif page == "EDA Insights":

    st.subheader("📊 Exploratory Data Analysis")

    tab1, tab2, tab3 = st.tabs(
        ["Mode Usage", "Peak Hours", "Travel Time"]
    )

    with tab1:
        show_image("mode_usage.png", "Transport Mode Usage")
        st.info("Bus transport dominates commuter preference, indicating high public transit dependency.")

    with tab2:
        show_image("peak_hours.png", "Peak Hour Analysis")
        st.info("Morning and evening commute peaks detected. Higher demand during work travel windows.")

    with tab3:
        show_image("travel_time.png", "Travel Time Distribution")
        st.info("Travel time spread indicates route delays and inconsistent trip durations.")

# ======================================================
# DEMAND PREDICTION
# ======================================================
elif page == "Demand Prediction":

    st.subheader("📈 Passenger Demand Forecast")

    show_image("demand_forecast.png", "24 Hour Demand Forecast")

    df = load_csv("predicted_demand.csv")

    if df is not None:

        st.dataframe(df, use_container_width=True)

        peak = df.loc[df["Predicted_Passengers"].idxmax()]

        st.success(
            f"Highest predicted demand at Hour {int(peak['hour'])}:00 "
            f"with {int(peak['Predicted_Passengers'])} passengers."
        )

        hour = st.slider("Select Hour", 0, 23, 9)

        val = df[df["hour"] == hour]["Predicted_Passengers"].values[0]

        st.metric(f"Predicted Demand at {hour}:00", int(val))

    else:
        st.warning("predicted_demand.csv not found.")

# ======================================================
# ROUTE OPTIMIZATION
# ======================================================
elif page == "Route Optimization":

    st.subheader("🛣 Optimized Routes")

    show_image("optimized_routes.png", "Best Efficient Routes")

    df = load_csv("optimized_routes.csv")

    if df is None:
        df = load_csv("best_routes.csv")

    if df is not None:

        st.dataframe(df, use_container_width=True)

        st.success(
            "Top routes selected using shortest distance, better speed limit, and lane efficiency."
        )

    else:
        st.warning("optimized route file not found.")

# ======================================================
# BUS ALLOCATION
# ======================================================
elif page == "Bus Allocation":

    st.subheader("🚍 Bus Allocation Recommendations")

    show_image("bus_allocation.png", "Recommended Buses Per Route")

    df = load_csv("bus_recommendation.csv")

    if df is not None:

        st.dataframe(df, use_container_width=True)

        top = df.loc[df["Passengers"].idxmax()]

        st.success(
            f"Route {top['Route']} has highest demand with "
            f"{int(top['Passengers'])} passengers."
        )

        route = st.selectbox("Select Route", df["Route"])

        row = df[df["Route"] == route].iloc[0]

        st.metric(
            f"Recommended Buses for Route {route}",
            int(row["Recommended_Buses"])
        )

    else:
        st.warning("bus_recommendation.csv not found.")

# ======================================================
# REPORTS
# ======================================================
elif page == "Reports & Downloads":

    st.subheader("📄 Project Outputs")

    files = [
        "predicted_demand.csv",
        "optimized_routes.csv",
        "best_routes.csv",
        "bus_recommendation.csv"
    ]

    for file in files:

        df = load_csv(file)

        st.markdown(f"### {file}")

        if df is not None:

            st.dataframe(df.head(10), use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label=f"Download {file}",
                data=csv,
                file_name=file,
                mime="text/csv",
                key=file
            )

        else:
            st.warning(f"{file} not found.")

        st.markdown("---")
