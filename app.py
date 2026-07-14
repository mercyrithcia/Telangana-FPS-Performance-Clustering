import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import folium
from streamlit_folium import st_folium

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Telangana Fair Price Shop Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("data/processed/clustered_dataset.csv")

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    return df

df = load_data()

# ==========================================================
# CLUSTER NAMES
# ==========================================================

cluster_names = {
    0: "🟢 High Performing Shops",
    1: "🔵 Medium Performing Shops",
    2: "🟡 Low Performing Shops",
    3: "🟠 Rare Behaviour Shops",
    4: "🔴 Outlier Shops"
}

df["Cluster_Name"] = df["Cluster"].map(cluster_names)

# ==========================================================
# TITLE
# ==========================================================

st.title("📊 Telangana Fair Price Shop Performance Dashboard")

st.markdown("""
This dashboard analyzes Telangana Fair Price Shops using
Machine Learning clustering, Exploratory Data Analysis,
and Geospatial Visualization.
""")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Dashboard Filters")

district = st.sidebar.selectbox(
    "District",
    ["All"] + sorted(df["distName"].dropna().unique().tolist())
)

month = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df["month"].dropna().unique().tolist())
)

cluster = st.sidebar.selectbox(
    "Cluster",
    ["All"] + list(cluster_names.values())
)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df.copy()

if district != "All":
    filtered = filtered[
        filtered["distName"] == district
    ]

if month != "All":
    filtered = filtered[
        filtered["month"] == month
    ]

if cluster != "All":
    filtered = filtered[
        filtered["Cluster_Name"] == cluster
    ]

if filtered.empty:
    st.warning("No records found for selected filters.")
    st.stop()

st.sidebar.markdown("---")

st.sidebar.info("""
### 📊 Project Summary

**Algorithm**
- PCA
- K-Means
- DBSCAN

**Dataset**
- Transactions
- Card Status
- FPS Locations

**Duration**
January 2025 - May 2025
""")

# ==========================================================
# KPI CARDS
# ==========================================================

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🏪 Total Shops",
        value=filtered["shopNo"].nunique()
    )

with col2:
    st.metric(
        label="📦 Total Transactions",
        value=f"{int(filtered['noOfTrans'].sum()):,}"
    )

with col3:
    st.metric(
        label="👨‍👩‍👧 Total Ration Cards",
        value=f"{int(filtered['totalRcs'].sum()):,}"
    )

with col4:
    st.metric(
        label="📈 Avg Utilization Ratio",
        value=f"{filtered['utilization_ratio'].mean():.2f}"
    )

# ==========================================================
# MONTHLY TRANSACTION TREND
# ==========================================================

st.markdown("---")

st.subheader("📈 Monthly Transaction Trend")

monthly = (
    filtered
    .groupby("month")["noOfTrans"]
    .sum()
    .reset_index()
)

fig = px.line(
    monthly,
    x="month",
    y="noOfTrans",
    markers=True,
    title="Monthly Transactions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# PORTABILITY TREND
# ==========================================================

st.markdown("---")

st.subheader("🚚 Other Shop Transactions (Portability)")

portability = (
    filtered
    .groupby("month")["otherShopTransCnt"]
    .sum()
    .reset_index()
)

fig = px.bar(
    portability,
    x="month",
    y="otherShopTransCnt",
    color="otherShopTransCnt",
    title="Portability Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# CLUSTER DISTRIBUTION
# ==========================================================

st.markdown("---")
st.subheader("📊 Shop Distribution by Cluster")

cluster_counts = (
    filtered["Cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = ["Cluster","Count"]

fig = px.bar(
    cluster_counts,
    x="Cluster",
    y="Count",
    color="Cluster",
    text="Count",
    title="Number of Shops in Each Cluster"
)

fig.update_traces(textposition="outside")

st.plotly_chart(fig,use_container_width=True)

# ==========================================================
# COMMODITY DISTRIBUTION
# ==========================================================

st.markdown("---")
st.subheader("🌾 Commodity Distribution")

commodity = pd.DataFrame({

    "Commodity":[
        "Rice",
        "Wheat",
        "Sugar",
        "Raghi Dal",
        "Salt",
        "Kerosene"
    ],

    "Quantity":[
        filtered["total_rice"].sum(),
        filtered["wheat"].sum(),
        filtered["sugar"].sum(),
        filtered["rgdal"].sum(),
        filtered["salt"].sum(),
        filtered["kerosene"].sum()
    ]

})

fig = px.pie(

    commodity,

    names="Commodity",

    values="Quantity",

    hole=0.45,

    title="Commodity Share"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# UTILIZATION RATIO
# ==========================================================

st.markdown("---")
st.subheader("📉 Average Utilization Ratio")

util = (

    filtered

    .groupby("Cluster")["utilization_ratio"]

    .mean()

    .reset_index()

)

fig = px.bar(

    util,

    x="Cluster",

    y="utilization_ratio",

    color="Cluster",

    text="utilization_ratio"

)

fig.update_traces(

    texttemplate="%{text:.2f}",

    textposition="outside"

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.markdown("---")
st.subheader("🔥 Feature Correlation")

corr_columns=[

    "noOfTrans",

    "totalRcs",

    "totalAmount",

    "utilization_ratio",

    "commodity_intensity",

    "portability_ratio"

]

corr=filtered[corr_columns].corr()

fig=go.Figure(

    data=go.Heatmap(

        z=corr.values,

        x=corr.columns,

        y=corr.columns,

        text=np.round(corr.values,2),

        texttemplate="%{text}",

        colorscale="RdBu",

        zmin=-1,

        zmax=1

    )

)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# PCA VISUALIZATION
# ==========================================================

if "PCA1" in filtered.columns and "PCA2" in filtered.columns:

    st.markdown("---")
    st.subheader("⭐ PCA Cluster Visualization")

    fig = px.scatter(

        filtered,

        x="PCA1",

        y="PCA2",

        color="Cluster",

        hover_data=["shopNo","distName"],

        title="K-Means Clusters after PCA"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("PCA columns not found. Save PCA1 and PCA2 into clustered_dataset.csv")

# ==========================================================
# DBSCAN OUTLIERS
# ==========================================================

if "DBSCAN_Cluster" in filtered.columns:

    st.markdown("---")
    st.subheader("🚨 DBSCAN Outlier Detection")

    dbscan_counts=(

        filtered["DBSCAN_Cluster"]

        .value_counts()

        .reset_index()

    )

    dbscan_counts.columns=["Cluster","Count"]

    fig=px.bar(

        dbscan_counts,

        x="Cluster",

        y="Count",

        color="Cluster",

        text="Count",

        title="DBSCAN Cluster Distribution"

    )

    fig.update_traces(textposition="outside")

    st.plotly_chart(

        fig,

        use_container_width=True

    )
outliers = (
    filtered["DBSCAN_Cluster"] == -1
).sum()

st.metric(
    "🚨 DBSCAN Outliers",
    outliers
)

# ==========================================================
# DBSCAN OUTLIER VISUALIZATION
# ==========================================================

if {"PCA1", "PCA2", "DBSCAN_Cluster"}.issubset(filtered.columns):

    st.markdown("---")
    st.subheader("🚨 DBSCAN Outlier Detection")

    fig = px.scatter(
        filtered,
        x="PCA1",
        y="PCA2",
        color=filtered["DBSCAN_Cluster"].astype(str),
        hover_data=["shopNo", "distName"],
        title="DBSCAN Clustering (Outliers shown separately)"
    )

    st.plotly_chart(fig, use_container_width=True)

    outliers = (filtered["DBSCAN_Cluster"] == -1).sum()

    st.info(f"🔍 Total Outlier Shops Detected: **{outliers}**")

else:

    st.warning("PCA1, PCA2 or DBSCAN_Cluster columns are missing.")

# ==========================================================
# GEOSPATIAL MAP
# ==========================================================

st.markdown("---")
st.subheader("🗺️ Telangana FPS Cluster Map")

map_df = filtered.copy()

map_df["latitude"] = pd.to_numeric(map_df["latitude"], errors="coerce")
map_df["longitude"] = pd.to_numeric(map_df["longitude"], errors="coerce")

map_df = map_df.dropna(subset=["latitude", "longitude"])

if len(map_df):

    center = [
        map_df["latitude"].mean(),
        map_df["longitude"].mean()
    ]

    m = folium.Map(
        location=center,
        zoom_start=7,
        tiles="CartoDB Positron"
    )

    colors = {
        "🟢 High Performing Shops":"green",
        "🔵 Medium Performing Shops":"blue",
        "🟡 Low Performing Shops":"orange",
        "🟠 Rare Behaviour Shops":"red",
        "🔴 Outlier Shops":"purple"
    }

    for _, row in map_df.iterrows():

        folium.CircleMarker(

            location=[row["latitude"], row["longitude"]],

            radius=4,

            color=colors.get(row["Cluster_Name"], "gray"),

            fill=True,

            fill_opacity=0.7,

            popup=f"""
            <b>Shop:</b> {row['shopNo']}<br>
            <b>District:</b> {row['distName']}<br>
            <b>Cluster:</b> {row['Cluster_Name']}<br>
            <b>Transactions:</b> {int(row['noOfTrans'])}
            """

        ).add_to(m)

    st_folium(
        m,
        width=1200,
        height=550
    )

else:

    st.warning("No valid coordinates available.")

# ==========================================================
# BUSINESS INSIGHTS
# ==========================================================

st.markdown("---")
st.subheader("💡 Business Insights")

st.success("""
           
### Key Findings

• High Performing Shops exhibit the highest utilization ratio and transaction volume.

• Medium Performing Shops operate consistently and require normal stock allocation.

• Low Performing Shops show lower beneficiary utilization and may require awareness initiatives.

• Rare Behaviour Shops display unusual transaction patterns and should be monitored periodically.

• DBSCAN outliers represent shops with exceptional behaviour that deserve detailed auditing.

### Recommendations

✅ Increase stock replenishment for high-demand shops.

✅ Monitor portability hubs more frequently.

✅ Investigate DBSCAN outliers for possible fraud or exceptional demand.

✅ Improve awareness and accessibility for low-performing shops.

✅ Continue monitoring cluster movements over time for policy evaluation.
""")

st.markdown("---")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=filtered.to_csv(index=False),
    file_name="Telangana_FPS_Filtered_Data.csv",
    mime="text/csv"
)

# ==========================================================
# DASHBOARD INFORMATION
# ==========================================================

st.markdown("---")
st.subheader("ℹ️ Dashboard Information")

st.info("""
This dashboard enables analysis of Telangana Fair Price Shop (FPS) performance
using Machine Learning clustering techniques.

Use the filters in the left sidebar to explore:

• District-wise performance
• Monthly transaction trends
• Cluster-wise analysis
• Geographical distribution of FPS shops
• Commodity utilization
• DBSCAN outlier detection

The dashboard provides interactive visual insights to support
data-driven decision-making.
""")
# ==========================================================
# CLUSTER PROFILE
# ==========================================================

st.markdown("---")

st.subheader("📋 Cluster Profile")

cluster_profile = (

    filtered

    .groupby("Cluster_Name")

    [

        [

            "noOfTrans",

            "totalRcs",

            "totalAmount",

            "utilization_ratio",

            "commodity_intensity",

            "portability_ratio"

        ]

    ]

    .mean()

    .round(2)

)

st.dataframe(
    cluster_profile,
    use_container_width=True
)

cluster_counts = (
    filtered["Cluster_Name"]
    .value_counts()
    .reset_index()
)

cluster_counts.columns = [
    "Cluster",
    "Count"
]

fig = px.pie(
    cluster_counts,
    names="Cluster",
    values="Count",
    title="Cluster Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ==========================================================
# DASHBOARD SUMMARY
# ==========================================================

st.markdown("---")

st.subheader("📊 Dashboard Summary")

c1,c2,c3 = st.columns(3)

c1.metric(
    "Clusters",
    filtered["Cluster"].nunique()
)

c2.metric(
    "Outliers",
    (filtered["DBSCAN_Cluster"]==-1).sum()
)

c3.metric(
    "Districts",
    filtered["distName"].nunique()
)

st.markdown("---")

st.caption(
"""
Telangana FPS Shop Clustering Dashboard

Developed using

Python • Pandas • Scikit-Learn • Streamlit • Folium • Plotly
"""
)