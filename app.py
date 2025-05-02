import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set wide layout for better visuals
st.set_page_config(layout="wide")

# Title and Description
st.title("📊 School Mode of Travel Dashboard")
st.markdown("""
Explore how students travel to school using data from the UK.  
This dashboard is built for policymakers to promote sustainable transport modes.
""")

# Load the dataset
df = pd.read_csv("mot_data.csv", encoding="ISO-8859-1")

# Clean dataset: Replace 'None' with 0 and convert columns to numeric
columns_to_fix = df.columns[2:]  # skip DfE and School Name
df[columns_to_fix] = df[columns_to_fix].replace('None', 0)
df[columns_to_fix] = df[columns_to_fix].apply(pd.to_numeric, errors='coerce')

# Sidebar filter
st.sidebar.header("🔎 Filter Data")
selected_school = st.sidebar.multiselect("Select School(s)", df["School Name"].unique())
filtered_df = df[df["School Name"].isin(selected_school)] if selected_school else df

# KPI summary
st.subheader("📌 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Students", int(filtered_df["Grand Total"].sum()))
col2.metric("Total Schools", filtered_df["School Name"].nunique())
most_common_mode = filtered_df.drop(columns=["DfE", "School Name", "Grand Total"]).sum().idxmax()
col3.metric("Most Common Mode", most_common_mode)

# Show data preview
st.subheader("🧾 Dataset Preview")
st.dataframe(filtered_df)

# Dropdown to select transport mode
transport_mode = st.selectbox("Select a transport mode:", df.columns[2:-1])
st.subheader(f"📊 Total Students Using {transport_mode} by School")

# Bar chart
mode_df = filtered_df[["School Name", transport_mode]]
mode_df = mode_df.sort_values(by=transport_mode, ascending=False)
st.bar_chart(mode_df.set_index("School Name"))

# Pie chart of overall mode distribution
st.subheader("🍩 Overall Transport Mode Distribution")
total_modes = filtered_df.drop(columns=["DfE", "School Name", "Grand Total"]).sum()
fig, ax = plt.subplots()
ax.pie(total_modes, labels=total_modes.index, autopct="%1.1f%%", startangle=90)
ax.axis("equal")
st.pyplot(fig)

# Top 10 schools by student population
st.subheader("🏫 Top 10 Schools by Student Count")
top_schools = filtered_df.sort_values(by="Grand Total", ascending=False).head(10)
st.dataframe(top_schools[["School Name", "Grand Total"]])

# Download data button
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name="filtered_school_travel_data.csv",
    mime='text/csv'
)
