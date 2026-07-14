# Telangana Fair Price Shop (FPS) Performance Clustering

## Project Report

---

# 1. Executive Summary

The Telangana State Civil Supplies Department manages thousands of Fair Price Shops (FPS) that distribute essential commodities under the Public Distribution System (PDS). Monitoring shop performance manually is difficult because of the large number of transactions, beneficiaries, and geographical locations.

This project applies Machine Learning clustering techniques to identify behavioral patterns among FPS shops, detect unusual transaction behavior, and provide an interactive Streamlit dashboard for visualization and decision-making.

---

# 2. Problem Statement

The objective of this project is to analyze Fair Price Shop performance using historical transaction, ration card, and geospatial data.

The project aims to:

- Identify similar groups of Fair Price Shops.
- Detect abnormal transaction patterns.
- Analyze portability trends under One Nation One Ration Card (ONORC).
- Support policy decisions using data-driven insights.

---

# 3. Objectives

- Merge multiple government datasets into a unified dataset.
- Perform Exploratory Data Analysis (EDA).
- Engineer meaningful features.
- Reduce dimensionality using PCA.
- Cluster FPS shops using K-Means.
- Detect anomalies using DBSCAN.
- Develop an interactive Streamlit dashboard.

---

# 4. Dataset Description

Three datasets were used:

## Transactions Dataset

Contains monthly FPS transaction information including:

- Number of transactions
- Commodity distribution
- Total amount
- Other Shop Transactions (Portability)

---

## Card Status Dataset

Contains:

- Number of ration cards
- Beneficiary units
- Card categories
- Entitlement details

---

## FPS Location Dataset

Contains:

- Shop Number
- District
- Latitude
- Longitude
- FPS Status

---

# 5. Data Preprocessing

The following preprocessing steps were performed:

- Missing value handling
- Duplicate removal
- Data type conversion
- Triple dataset merge
- Feature scaling using StandardScaler

---

# 6. Exploratory Data Analysis

EDA was performed to understand transaction behavior.

Visualizations included:

- Monthly Transaction Trend
- Portability Trend
- Commodity Distribution
- District-wise Distribution
- Correlation Heatmap
- Utilization Analysis

Key observations:

- Rice constituted the highest distributed commodity.
- Portability transactions increased during the observed period.
- Higher ration card counts generally corresponded to higher transaction volumes.

---

# 7. Feature Engineering

The following features were created:

## Utilization Ratio

Transactions / Total Ration Cards

Measures how efficiently beneficiaries utilize FPS services.

---

## Portability Ratio

Other Shop Transactions / Total Transactions

Measures ONORC portability usage.

---

## Rice-Wheat Ratio

Rice Distribution / Wheat Distribution

Measures commodity preference.

---

## Commodity Intensity

Combined commodity distribution indicator.

---

## Amount per Card

Total Amount / Total Ration Cards

---

## Units per Card

Total Units / Total Ration Cards

---

# 8. Principal Component Analysis (PCA)

PCA was used to reduce the dimensionality of multiple numerical variables into two principal components.

Benefits:

- Reduced feature complexity
- Improved visualization
- Better cluster separation

The first two principal components captured the majority of the data variance.

---

# 9. K-Means Clustering

K-Means clustering segmented Fair Price Shops into five behavioral groups.

The optimal number of clusters was selected using:

- Elbow Method
- Silhouette Score

Cluster interpretation:

| Cluster | Description |
|----------|-------------|
| 0 | High Performing Shops |
| 1 | Medium Performing Shops |
| 2 | Low Performing Shops |
| 3 | Rare Behaviour Shops |
| 4 | Outlier Shops |

---

# 10. DBSCAN

DBSCAN was used to detect anomalous FPS shops.

Advantages:

- No need to specify cluster count
- Detects irregular transaction behavior
- Identifies noise points

Potential outliers may indicate:

- Ghost beneficiaries
- Stock diversion
- Exceptional demand
- Data inconsistencies

---

# 11. Streamlit Dashboard

The dashboard includes:

- District Filter
- Month Filter
- Cluster Filter
- KPI Cards
- Monthly Trend
- Portability Trend
- Commodity Distribution
- Cluster Distribution
- Utilization Ratio
- Correlation Heatmap
- PCA Visualization
- DBSCAN Visualization
- Interactive Telangana Map
- Shop Search
- Cluster Profile
- Download Filtered Dataset

---

# 12. Results

The clustering model successfully segmented FPS shops into meaningful groups.

The dashboard enables:

- Identification of high-performing shops
- Detection of abnormal shops
- Better stock planning
- Improved geographical analysis
- Policy evaluation

---

# 13. Business Recommendations

Based on the analysis:

- Increase stock allocation to high-performing shops.
- Monitor portability hubs regularly.
- Audit DBSCAN outlier shops.
- Improve awareness in low-utilization regions.
- Continue periodic cluster monitoring.

---

# 14. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Plotly
- Scikit-Learn
- PCA
- K-Means
- DBSCAN
- Streamlit
- Folium

---

# 15. Conclusion

This project demonstrates how Machine Learning can improve the monitoring of Fair Price Shops by identifying behavioral patterns and operational anomalies.

The developed dashboard provides an interactive platform for policymakers to analyze shop performance, improve logistics planning, detect unusual behavior, and support data-driven decision-making.

Future enhancements may include predictive analytics, real-time monitoring, and demand forecasting.

---

# Author

**Mercy Rithcia**

Aspiring Data Analyst

Python | SQL | Power BI | Machine Learning