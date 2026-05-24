import streamlit as st
st.set_page_config(layout="wide")

import plotly.graph_objects as go
import joblib
import pandas as pd
import numpy as np
import gdown
import os



# ---------------- HEADER ----------------
col1, col2 = st.columns([4.5,8])

with col2:
    st.markdown("""
    <h1 style='
        text-align:left;
        color:#60A5FA;
        font-weight:700;
        margin-top: 20px;
        letter-spacing:1px; 
    '>
    Real Estate Dashboard
    </h1>
    """, unsafe_allow_html=True)

with col1:
    st.image("image.png", width=300)


# ---------------- SIDEBAR ----------------
# Sidebar Logo
col10, col11, col12 = st.sidebar.columns([1,10,1])

with col11:
    st.image("image.png", use_container_width=True)

# Sidebar Heading
st.sidebar.markdown("""
<h2 style='color:#60A5FA; text-align:center;'>
Dashboard Filters
</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.markdown(
    "<hr style='border:1px solid #1f2937'>",
    unsafe_allow_html=True
)


# ---------------- LOAD MODEL ----------------
# Load Trained Model and Metadata
model = joblib.load("xgb_model.joblib")

metadata = joblib.load("xgb_metadata.joblib")

feature_names = metadata["feature_names"]

binary_cols = metadata["binary_cols"]

cities = metadata["cities"]

location_map = metadata["location_map"]

area_min, area_max = metadata["area_range"]

st.sidebar.markdown("Property Basics")


# ---------------- INPUTS ----------------
# City Selection
city = st.sidebar.selectbox(
    "Select City",
    cities
)

# Location Selection
location = st.sidebar.selectbox(
    "Select Location",
    location_map[city]
)

# Input Type Selection
choice = st.sidebar.radio(
    "Select Input Type",
    ["Slider", "Manual Input"]
)

# Area Input
if choice == "Slider":

    area = st.sidebar.slider(
        "Area sq.ft",
        area_min,
        area_max,
        1000
    )

else:

    area = st.sidebar.number_input(
        "Area sq.ft",
        min_value=area_min,
        max_value=area_max,
        value=1000,
        step=1
    )

# Bedroom Input
bedroom = st.sidebar.slider(
    "Number of Bedrooms",
    1,
    10,
    2
)


# ---------------- AMENITIES ----------------
# Amenities Selection
st.sidebar.markdown("Amenities")

selected_amenities = [

    # Essential Amenities
    "24X7Security",
    "PowerBackup",
    "CarParking",
    "LiftAvailable",

    # Internet & Utility
    "Wifi",
    "Gasconnection",

    # Lifestyle Amenities
    "Gymnasium",
    "SwimmingPool",
    "ClubHouse",
    "AC",

    # Nearby Facilities
    "ATM",
    "School"
]

binary_inputs = {}

# Create Checkboxes
for feature in selected_amenities:

    display_name = (
        feature
        .replace("24X7", "24x7 ")
        .replace("Children'splayarea", "Children Play Area")
    )

    binary_inputs[feature] = st.sidebar.checkbox(
        display_name
    )


# ---------------- MODEL INPUT ----------------
# Create Input Dictionary
input_data = dict.fromkeys(feature_names, 0)

# Basic Features
input_data["Area"] = area
input_data["No. of Bedrooms"] = bedroom

# Amenities Encoding
for feature in selected_amenities:

    input_data[feature] = int(
        binary_inputs[feature]
    )

# Feature Engineering
input_data["AmenityScore"] = sum(
    input_data[col]
    for col in selected_amenities
)


# ---------------- LOCATION ENCODING ----------------
# Encode Selected Location
location_means = metadata["location_means"]

input_data["Location_Encoded"] = location_means.get(
    location,
    0
)


# ---------------- CREATE DATAFRAME ----------------
# Create Prediction DataFrame
input_df = pd.DataFrame([input_data])

# Match Model Training Columns
input_df = input_df[feature_names]


# ---------------- PREDICTION ----------------
# Predict Property Price
price = model.predict(input_df)[0]


# ---------------- SAFETY ----------------
# Handle Invalid Predictions
if np.isnan(price) or np.isinf(price):
    price = 0

price = max(price, 0)


# ---------------- DISPLAY ---------------
# Prediction Heading
st.markdown("""
<h2 style='color:#60A5FA; text-align:center'>
What-If Price Calculator
</h2>

<p style='color:#9CA3AF; text-align:center'>
Adjust inputs in the sidebar to see real-time price prediction
</p>
""", unsafe_allow_html=True)


# Predicted Price Display
st.markdown(f"""
<h1 style='
text-align:center;
color:#60A5FA;
text-shadow: 0px 0px 20px rgba(96,165,250,0.6);
'>
₹ {price:,.0f}
</h1>
""", unsafe_allow_html=True)


# ---------------- GAUGE ----------------
# Price Gauge Chart
def price_gauge(price):

    max_val = 35000000

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=price,
        number={'valueformat': ',d'},
        title={'text': "Price Level"},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': "#EBF4FE"},
            'steps': [
                {'range': [0, max_val*0.2], 'color': "#afccf1"},
                {'range': [max_val*0.2, max_val*0.4], 'color': "#93c5fd"},
                {'range': [max_val*0.4, max_val*0.6], 'color': "#60a5fa"},
                {'range': [max_val*0.6, max_val*0.8], 'color': "#2563eb"},
                {'range': [max_val*0.8, max_val], 'color': "#1e3a8a"},
            ]
        }
    ))

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )

    return fig


# Gauge Layout
col1, col2, col3 = st.columns([1,2,1])

with col2:
    st.plotly_chart(price_gauge(price))


# ---------------- CARDS ----------------
# Information Cards
def card(title, value):

    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e3a5f, #0f2a3f);
        padding:25px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius:40px;
        text-align:center;
        box-shadow: 0px 6px 25px rgba(0,0,0,0.6);
    ">
        <h4 style="color:#9CA3AF;">{title}</h4>
        <h1 style="color:white;">{value}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    "<hr style='border:1px solid #1f2937'>",
    unsafe_allow_html=True
)


# Cards Layout
col3, col4, col5 = st.columns(3)

with col3:
    card("Average price", f"₹ {int(price*0.8):,}")

with col4:
    card("Max Price", f"₹ {int(price*1.2):,}")

with col5:
    card("Min Price", f"₹ {int(price*0.6):,}")

st.markdown(
    "<hr style='border:1px solid #1f2937'>",
    unsafe_allow_html=True
)


# ---------------- CHARTS ----------------
# Section Heading
st.markdown("""
<h2 style='color:#60A5FA;'>
Amenities vs Property Price
</h2>
""", unsafe_allow_html=True)


# ---------------- LOAD DATASET ----------------
# Load Dataset
df = pd.read_csv("real_estate_cleaned.csv")

# Filter Dataset According to Selected City
df = df[df["City"] == city]

# Create Total Amenities Column
df["Total_Amenities"] = df[binary_cols].sum(axis=1)

# Create Price per Sqft Column
df["Price_per_sqft"] = df["Price"] / df["Area"]


# ---------------- CHART 1 ----------------
# Amenities vs Price Chart
amenity_price = (
    df.groupby("Total_Amenities")["Price"]
    .mean()
)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=amenity_price.index,
    y=amenity_price.values,
    mode='lines+markers'
))

fig.update_layout(
    title=f"Average Property Price by Amenities - {city}",

    font=dict(color="white"),

    xaxis=dict(
        title="Number of Amenities",
    ),

    yaxis=dict(
        title="Average Price",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- CHART 2 ----------------
# Price per Sqft by Location
location_price = (
    df.groupby("Location")["Price_per_sqft"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=location_price.index,
    y=location_price.values,
    marker_color="#60A5FA"
))

fig.update_layout(
    title=f"Average Price per Sqft by Location - {city}",

    xaxis=dict(
        title="Location",
    ),

    yaxis=dict(
        title="Price per Sqft",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)


# ---------------- CHART 3 ----------------
# Area vs Property Price Scatter Plot
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Area"],
    y=df["Price"],

    mode='markers',

    marker=dict(
        size=8,
        color="#60A5FA",
        opacity=0.7
    )
))

fig.update_layout(
    title=f"Area vs Property Price - {city}",

    xaxis=dict(
        title="Area (sq.ft)",
    ),

    yaxis=dict(
        title="Property Price",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)




















