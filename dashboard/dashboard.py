import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
data = pd.read_csv("main_data2.csv")

# Set page configuration
st.set_page_config(page_title="Bike Rentals Dashboard", layout="wide")
st.title("Bike Rentals Dashboard")

# Sidebar: Pilih Pertanyaan yang Akan Ditampilkan
st.sidebar.header("Select Analysis Question")
question = st.sidebar.radio(
    "Choose an analysis to view:",
    ("Average Rentals by Season", 
     "Average Rentals by Hour", 
     "Average Rentals by Day Type", 
     "Correlation Between Variables", 
     "Average Usage (Daily and Hourly)")
)

# Filter data based on selected question
if question == "Average Rentals by Season":
    filtered_data = data[data["Description"] == "Average Rentals by Season"]
    st.header("Average Rentals by Season")
    fig = px.bar(
        filtered_data,
        x="Category",
        y="Value",
        color="Description",
        title="Average Bike Rentals by Season"
    )
    st.plotly_chart(fig)

elif question == "Average Rentals by Hour":
    filtered_data = data[data["Description"] == "Average Rentals by Hour"]
    st.header("Average Rentals by Hour")
    fig = px.line(
        filtered_data,
        x="Category",
        y="Value",
        color="Description",
        title="Average Bike Rentals by Hour"
    )
    st.plotly_chart(fig)

elif question == "Average Rentals by Day Type":
    filtered_data = data[data["Description"] == "Average Rentals by Day Type"]
    st.header("Average Rentals by Day Type")
    fig = px.bar(
        filtered_data,
        x="Category",
        y="Value",
        color="Description",
        title="Average Bike Rentals by Day Type"
    )
    st.plotly_chart(fig)

elif question == "Correlation Between Variables":
    filtered_data = data[data["Description"] == "Correlation Between Variables"]
    st.header("Correlation Between Weather Variables and Bike Rentals")
    fig = px.scatter(
        filtered_data,
        x="Value", 
        y="Subcategory",
        color="Category",
        title="Correlation Between Weather Variables and Bike Rentals"
    )
    st.plotly_chart(fig)

elif question == "Average Usage (Daily and Hourly)":
    filtered_data = data[data["Description"] == "Average Usage (Daily and Hourly)"]
    st.header("Average Bike Usage (Daily and Hourly)")
    fig = px.bar(
        filtered_data,
        x="Category",
        y="Value",
        color="Subcategory",
        title="Average Bike Usage: Daily vs Hourly"
    )
    st.plotly_chart(fig)

# Sidebar message
st.sidebar.write("Select an analysis question to explore the data.")
